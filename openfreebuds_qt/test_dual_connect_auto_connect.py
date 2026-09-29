"""LibreBuds: the auto-connect checkbox stays disabled when the device does not report it."""
import asyncio
import contextlib
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

pytest.importorskip("PyQt6")

from openfreebuds_qt.app.module import dual_connect as module
from openfreebuds_qt.app.module.dual_connect import OfbQtDualConnectModule


@contextlib.asynccontextmanager
async def _raise_errors(identifier, ctx):
    yield


def _device(**extra):
    return {"name": "Laptop", "connected": True, "playing": False, "preferred": False, **extra}


def _run_update(monkeypatch, devices):
    monkeypatch.setattr(module, "qt_error_handler", _raise_errors)
    monkeypatch.setattr(module, "create_dual_connect_icon", MagicMock())
    monkeypatch.setattr(module, "ImageQt", MagicMock())
    monkeypatch.setattr(module, "QIcon", MagicMock())
    monkeypatch.setattr(module, "QListWidgetItem", MagicMock())

    devices_list = MagicMock()
    devices_list.currentRow.return_value = 0
    view = SimpleNamespace(
        ctx=None,
        ofb=SimpleNamespace(get_property=AsyncMock(return_value={
            "enabled": "true",
            "unpair_supported": "false",
            "devices": json.dumps(devices),
        })),
        _current_index=-1,
        _all_data=[],
        list_item=MagicMock(),
        button_unpair=MagicMock(),
        global_toggle=MagicMock(),
        devices_list=devices_list,
        button_toggle_connect=MagicMock(),
        current_device_auto_connect=MagicMock(),
        current_device_prefered=MagicMock(),
        refresh_button=MagicMock(),
    )
    event = SimpleNamespace(is_changed=lambda group, prop=None: True)
    asyncio.run(OfbQtDualConnectModule.update_ui(view, event))
    return view


def test_auto_connect_stays_disabled_without_flag(monkeypatch):
    view = _run_update(monkeypatch, {"001122334455": _device()})
    view.current_device_auto_connect.setEnabled.assert_called_with(False)
    view.button_toggle_connect.setEnabled.assert_called_with(True)


def test_auto_connect_enabled_when_reported(monkeypatch):
    view = _run_update(monkeypatch, {"001122334455": _device(auto_connect=False)})
    view.current_device_auto_connect.setEnabled.assert_called_with(True)
