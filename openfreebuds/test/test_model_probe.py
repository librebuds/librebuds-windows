"""Model detection by reported model code when the Bluetooth name is unknown."""
import asyncio

import pytest

from openfreebuds.driver.huawei.driver.generic import OfbDriverHuaweiGeneric
from openfreebuds.driver.huawei.driver.per_model.buds_6 import OfbDriverHuawei6
from openfreebuds.exceptions import OfbNotSupportedError
from openfreebuds.manager.main import OfbManager


class _FakeWriter:
    def __init__(self):
        self.closed = False
        self.wait_closed_called = False

    def close(self):
        self.closed = True

    async def wait_closed(self):
        self.wait_closed_called = True


def _patch_probe(monkeypatch, *, model=None, fail=False, events=None):
    writers = []

    async def fake_start(self):
        events.append("start")
        if fail:
            raise OSError("connect failed")
        self._writer = _FakeWriter()
        writers.append(self._writer)
        self.started = True
        if model is not None:
            await self.put_property("info", "device_model", model)

    async def fake_stop(self):
        events.append("stop")
        if self._writer is not None:
            self._writer.close()
        self._writer = None
        self.started = False

    monkeypatch.setattr(OfbDriverHuaweiGeneric, "start", fake_start)
    monkeypatch.setattr(OfbDriverHuaweiGeneric, "stop", fake_stop)
    return writers


def test_probe_returns_driver_and_closes_socket(monkeypatch):
    events = []
    writers = _patch_probe(monkeypatch, model="BTFT0020", events=events)
    cls = asyncio.run(OfbManager()._probe_model("00:11:22:33:44:55"))
    assert cls is OfbDriverHuawei6
    assert events == ["start", "stop"]
    assert writers[0].closed and writers[0].wait_closed_called


def test_probe_unknown_code(monkeypatch):
    events = []
    _patch_probe(monkeypatch, model="NOPE", events=events)
    assert asyncio.run(OfbManager()._probe_model("00:11:22:33:44:55")) is None
    assert events == ["start", "stop"]


def test_probe_failure_never_raises(monkeypatch):
    events = []
    _patch_probe(monkeypatch, fail=True, events=events)
    assert asyncio.run(OfbManager()._probe_model("00:11:22:33:44:55")) is None
    assert events == ["start", "stop"]


def test_start_unknown_name_falls_back_to_not_supported(monkeypatch):
    async def no_model(self, address):
        return None

    monkeypatch.setattr(OfbManager, "_probe_model", no_model)

    async def run():
        with pytest.raises(OfbNotSupportedError):
            await OfbManager().start("Some Headset", "00:11:22:33:44:55")

    asyncio.run(run())


def test_start_unknown_name_uses_probed_driver(monkeypatch):
    async def probed(self, address):
        return OfbDriverHuawei6

    async def idle_mainloop(self):
        pass

    monkeypatch.setattr(OfbManager, "_probe_model", probed)
    monkeypatch.setattr(OfbManager, "_mainloop", idle_mainloop)

    async def run():
        m = OfbManager()
        await m.start("Some Headset", "00:11:22:33:44:55")
        await asyncio.sleep(0)
        try:
            assert isinstance(m._driver, OfbDriverHuawei6)
            assert await m.get_device_tags() == ("Some Headset", "00:11:22:33:44:55")
        finally:
            await m.stop()

    asyncio.run(run())


def test_remote_error_keeps_class_name():
    from openfreebuds.utils.stupid_rpc import RemoteError

    e = RemoteError({"trace": "", "args": ["Unknown device"], "class": "OfbNotSupportedError"})
    assert e.rpc_class == "OfbNotSupportedError"
