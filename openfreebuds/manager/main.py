import asyncio
from asyncio import Task
from contextlib import asynccontextmanager, suppress
from typing import Optional

from aiohttp.web_routedef import RouteTableDef

from openfreebuds import webserver
from openfreebuds.constants import OfbEventKind
from openfreebuds.driver import DEVICE_TO_DRIVER_MAP
from openfreebuds.driver.generic import OfbDriverGeneric
from openfreebuds.exceptions import OfbNoDeviceError, OfbDriverError, OfbNotSupportedError
from openfreebuds.manager.generic import IOpenFreebuds
from openfreebuds.shortcuts import OfbShortcuts
from openfreebuds.utils.logger import create_logger, get_full_log
from openfreebuds.utils.stupid_rpc import rpc

log = create_logger("OfbManager")


class OfbManager(IOpenFreebuds):
    def __init__(self):
        super().__init__()
        self._driver: Optional[OfbDriverGeneric] = None
        self._task: Optional[Task] = None
        self._device_tags: tuple[str, str] = "", ""
        self._paused = False
        self._shortcuts = OfbShortcuts(self)

        self._state = IOpenFreebuds.STATE_STOPPED  # type: int
        self.role: str = "standalone"
        self.rpc_config: dict = {}
        self.server_task: Task | None = None

    @rpc
    async def get_state(self) -> int:
        return self._state

    @rpc
    async def get_logs(self) -> str:
        return get_full_log()

    @rpc
    async def get_health_report(self):
        driver_report = {} if not self._driver else await self._driver.get_health_report()

        return {
            **driver_report,
            "device_name": self._device_tags[0],
            "paused": self._paused,
            "state": self._state,
            "server_task_alive": not self.server_task.done(),
            "main_task_alive": not self._task.done()
        }

    @rpc
    async def start(self, device_name: str, device_address: str):
        """
        Start the driver for a device. Returns the profile name in use: the
        given name when it is a known profile, otherwise (LibreBuds) the
        profile detected from the model code the earbuds report. Callers
        should save the returned name so later starts need no probe.
        """
        await self.stop()
        profile_name = device_name
        driver_cls = DEVICE_TO_DRIVER_MAP.get(device_name)
        if driver_cls is None:
            driver_cls = await self._probe_model(device_address)
            profile_name = _profile_name_for_driver(driver_cls)
        if driver_cls is None or profile_name is None:
            raise OfbNotSupportedError(f"Unknown device {device_name}")

        self._driver = driver_cls(device_address)
        self.include_subscription("inner_driver", self._driver.changes)
        self._task = asyncio.create_task(self._mainloop())
        self._device_tags = profile_name, device_address
        return profile_name

    async def _probe_model(self, address: str):
        """
        LibreBuds: connect with an info-only driver and choose a driver by the
        model code the earbuds report. Never raises; returns None when the
        probe fails or the code is unknown.
        """
        from openfreebuds.driver.huawei.driver.generic import OfbDriverHuaweiGeneric
        from openfreebuds.driver.huawei.handler import OfbHuaweiInfoHandler
        from openfreebuds.driver.huawei.model_codes import driver_for_model_code

        probe = OfbDriverHuaweiGeneric(address)
        # SPEC-GAP: RFCOMM channel not confirmed for every model; channel 1 matches the known ones.
        probe._spp_service_port = 1
        probe.handlers = [OfbHuaweiInfoHandler()]
        code = None
        writer = None
        try:
            await asyncio.wait_for(probe.start(), timeout=10)
            writer = probe._writer
            code = await probe.get_property("info", "device_model", None)
        except Exception as e:
            log.info(f"Model probe failed: {e}")
        finally:
            writer = writer or probe._writer
            with suppress(Exception):
                await probe.stop()
            # Windows allows one RFCOMM socket per service per host, so the probe
            # socket must be fully closed before the real driver connects.
            if writer is not None:
                with suppress(Exception):
                    writer.close()
                    await asyncio.wait_for(writer.wait_closed(), timeout=2)
                await asyncio.sleep(0.5)

        driver_cls = driver_for_model_code(code)
        log.info(f"Model probe: code={code}, driver={driver_cls.__name__ if driver_cls else None}")
        return driver_cls

    @rpc
    async def destroy(self):
        log.debug("Destroying core...")
        await self.stop(IOpenFreebuds.STATE_DESTROYED)
        if self.server_task is not None:
            self.server_task.cancel("stop() requested")
            await self.server_task
        log.info("Bye-bye")

    @rpc
    async def stop(self, e_state: int = IOpenFreebuds.STATE_STOPPED):
        await self._set_state(e_state)
        if self._task is None:
            return

        log.debug("Stopping core...")
        self._task.cancel("stop() requested")
        await self._task

        if self._driver is not None:
            log.debug("Stopping driver...")
            await self._driver.stop()

        self._driver = None
        self._task = None
        self._device_tags = "", ""
        log.info("Stopped")

    @rpc
    async def get_device_tags(self):
        return self._device_tags

    @rpc
    async def get_property(self, group: str = None, prop: str = None, fallback=None):
        if not self._driver:
            return fallback
        return await self._driver.get_property(group, prop, fallback)

    @rpc
    async def set_property(self, group: str, prop: str, value: str):
        if self._driver is None:
            raise OfbNoDeviceError("Attempt to write prop without device")
        await self._driver.set_property(group, prop, value)

    @rpc
    async def run_shortcut(self, *args, no_catch: bool = False):
        log.info(f"Execute shortcut action {args}")
        return await self._shortcuts.execute(*args, no_catch=no_catch)

    @asynccontextmanager
    async def locked_device(self):
        try:
            await self._set_paused(True)
            yield
        finally:
            await self._set_paused(False)

    @rpc
    async def _set_paused(self, value: bool):
        log.debug(f"Core pause value={value}")
        self._paused = value
        await self._set_state(IOpenFreebuds.STATE_PAUSED)
        if value and self._driver.started:
            await self._driver.stop()

    async def _mainloop(self):
        with suppress(asyncio.CancelledError):
            await self._mainloop_inner()

    async def _mainloop_inner(self):
        log.debug(f"Started mainloop task")
        last_device_address = ""

        while True:
            if self._paused:
                await asyncio.sleep(2)
                continue

            if not await self._driver.is_device_online():
                await self._set_state(IOpenFreebuds.STATE_DISCONNECTED)
                if self._driver.started:
                    log.info("Device disconnected from OS")
                    await self._driver.stop()
                await asyncio.sleep(10)
                continue

            if not self._driver.started:
                log.info("Trying to start driver")
                await self._set_state(IOpenFreebuds.STATE_WAIT)
                try:
                    await self._driver.start()
                    await self._set_state(IOpenFreebuds.STATE_CONNECTED)
                    if last_device_address != self._device_tags[1]:
                        await self.send_message(OfbEventKind.DEVICE_CHANGED)
                        last_device_address = self._device_tags[1]
                except OfbDriverError as e:
                    log.error(f"Driver start failure: {e}, will retry in 5s")
                    await self._set_state(IOpenFreebuds.STATE_FAILED)
                    await asyncio.sleep(5)
                    continue
                except Exception:
                    log.exception("Unknown error while trying to start driver")

            if not self._driver.healthy():
                log.warning("Driver health check failed, restarting them")
                await self._driver.stop()

            await asyncio.sleep(2)

    def on_rpc_server_setup(self, routes: RouteTableDef, secret: Optional[str]):
        webserver.setup_routes(self, routes, secret)

    async def _set_state(self, new_state: int):
        if self._state == new_state:
            return

        self._state = new_state
        await self.send_message(OfbEventKind.STATE_CHANGED, new_state)


def _profile_name_for_driver(driver_cls):
    """First DEVICE_TO_DRIVER_MAP key that uses this driver class, or None."""
    if driver_cls is None:
        return None
    for name, cls in DEVICE_TO_DRIVER_MAP.items():
        if cls is driver_cls:
            return name
    return None
