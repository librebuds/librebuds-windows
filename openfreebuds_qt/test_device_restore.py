"""LibreBuds: saved profile names, boot tolerance and single device selection."""
import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

pytest.importorskip("PyQt6")

from openfreebuds.exceptions import OfbNotSupportedError
from openfreebuds_qt.app.module.choose_device import OfbQtChooseDeviceModule
from openfreebuds_qt.main import OfbQtApplication

ADDR = "00:11:22:33:44:55"


def _app(start):
    values = {("device", "name"): "Some Headset", ("device", "address"): ADDR}
    config = MagicMock()
    config.get.side_effect = lambda group, key, fallback=None: values.get((group, key), fallback)
    return SimpleNamespace(
        args=SimpleNamespace(virtual_device=None, shortcut="x"),
        config=config,
        ofb=SimpleNamespace(start=start, role="standalone", get_state=AsyncMock(), run_shortcut=AsyncMock()),
        _exit=MagicMock(),
    )


def test_restore_device_tolerates_start_failure():
    app = _app(AsyncMock(side_effect=OfbNotSupportedError("Unknown device Some Headset")))
    assert asyncio.run(OfbQtApplication.restore_device(app)) is False
    app.config.save.assert_not_called()


def test_restore_device_saves_detected_profile():
    app = _app(AsyncMock(return_value="HUAWEI FreeBuds 6"))
    assert asyncio.run(OfbQtApplication.restore_device(app)) is True
    app.config.set_device_data.assert_called_once_with("HUAWEI FreeBuds 6", ADDR)
    app.config.save.assert_called_once()


def test_shortcut_exits_when_device_cannot_start():
    app = _app(AsyncMock(side_effect=OfbNotSupportedError("x")))
    app.restore_device = lambda: OfbQtApplication.restore_device(app)
    asyncio.run(OfbQtApplication._stage_shortcut(app))
    app._exit.assert_called_once_with(1)
    app.ofb.run_shortcut.assert_not_called()


def _module(start):
    return SimpleNamespace(
        _select_busy=False,
        _connect_task=None,
        paired_list=MagicMock(),
        ofb=SimpleNamespace(start=start),
        config=MagicMock(),
        _update_list=AsyncMock(),
    )


def test_select_saves_detected_profile_and_ignores_reentry():
    release = asyncio.Event()
    calls = []

    async def start(name, address):
        calls.append(name)
        await release.wait()
        return "HUAWEI FreeBuds 6"

    mod = _module(start)

    async def run():
        first = asyncio.create_task(OfbQtChooseDeviceModule._select_device(mod, "Some Headset", ADDR))
        await asyncio.sleep(0)
        # Second click while the probe runs: ignored, no second start.
        await OfbQtChooseDeviceModule._select_device(mod, "Some Headset", ADDR)
        mod.paired_list.setEnabled.assert_called_with(False)
        release.set()
        await first

    asyncio.run(run())
    assert calls == ["Some Headset"]
    mod.config.set_device_data.assert_called_once_with("HUAWEI FreeBuds 6", ADDR)
    assert mod._select_busy is False
    mod.paired_list.setEnabled.assert_called_with(True)
