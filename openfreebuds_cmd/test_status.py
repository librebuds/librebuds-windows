import asyncio
import json
from unittest.mock import AsyncMock

from openfreebuds import IOpenFreebuds
from openfreebuds_cmd.main import OpenFreebudsCmd


def test_status_prints_dual_connect_flags_and_devices(capsys):
    store = {
        "dual_connect": {
            "enabled": "true",
            "preferred_device": "001122334455",
            "unpair_supported": "false",
            "devices": json.dumps({"001122334455": {"name": "Laptop", "connected": True}}),
        },
    }
    cmd = OpenFreebudsCmd.__new__(OpenFreebudsCmd)
    cmd.manager = AsyncMock()
    cmd.manager.get_state.return_value = IOpenFreebuds.STATE_CONNECTED
    cmd.manager.get_property.return_value = store

    asyncio.run(cmd.do_status())
    out = capsys.readouterr().out
    assert "unpair_supported" in out and "false" in out
    assert "001122334455" in out and "Laptop" in out
