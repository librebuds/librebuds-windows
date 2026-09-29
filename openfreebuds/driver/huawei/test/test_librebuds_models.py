import asyncio

import pytest

from openfreebuds.driver import DEVICE_TO_DRIVER_MAP, is_device_supported
from openfreebuds.driver.huawei.driver.per_model.buds_4 import OfbDriverHuawei4
from openfreebuds.driver.huawei.driver.per_model.buds_5 import OfbDriverHuawei5
from openfreebuds.driver.huawei.driver.per_model.buds_6 import OfbDriverHuawei6
from openfreebuds.driver.huawei.driver.per_model.buds_pro_2 import OfbDriverHuaweiPro2
from openfreebuds.driver.huawei.driver.per_model.buds_pro_3 import OfbDriverHuaweiPro3
from openfreebuds.driver.huawei.handler import (
    OfbHuaweiLowLatencyPreferenceHandler,
    OfbHuaweiVoiceLanguageHandler,
)
from openfreebuds.driver.huawei.handler.dual_connect import OfbHuaweiDualConnectNoUnpairHandler
from openfreebuds.driver.huawei.model_codes import driver_for_model_code
from openfreebuds.exceptions import OfbNotSupportedError

ROUND2_HANDLERS = [
    "device_info",
    "battery",
    "anc_global",
    "gesture_double",
    "gesture_triple",
    "gesture_long_split",
    "gesture_swipe",
    "tws_auto_pause",
    "config_eq",
    "dual_connect",
]


@pytest.mark.parametrize("name,cls,handler_ids", [
    ("HUAWEI FreeBuds 4", OfbDriverHuawei4, ["device_info", "battery", "anc_global"]),
    ("HUAWEI FreeBuds 5", OfbDriverHuawei5, ROUND2_HANDLERS),
    ("HUAWEI FreeBuds 6", OfbDriverHuawei6, ROUND2_HANDLERS),
])
def test_new_drivers(name, cls, handler_ids):
    assert is_device_supported(name)
    assert DEVICE_TO_DRIVER_MAP[name] is cls
    d = cls("00:11:22:33:44:55")
    assert d._spp_service_port == 1
    assert [h.handler_id for h in d.handlers] == handler_ids


@pytest.mark.parametrize("cls", [OfbDriverHuawei4, OfbDriverHuawei5, OfbDriverHuawei6])
def test_no_unconfirmed_handlers(cls):
    d = cls("00:11:22:33:44:55")
    for h in d.handlers:
        assert not isinstance(h, OfbHuaweiLowLatencyPreferenceHandler)
        assert not isinstance(h, OfbHuaweiVoiceLanguageHandler)
        assert h.handler_id not in ("low_latency", "voice_language", "tws_in_ear",
                                    "anc_change", "config_sound_quality")
        # 2B/03 and 2B/21 returned errors in round 2; 2B/6C (low latency) too.
        for cmd in list(h.commands) + list(h.ignore_commands):
            assert cmd not in (b"\x2b\x03", b"\x2b\x21", b"\x2b\x6c", b"\x0c\x01")


@pytest.mark.parametrize("cls", [OfbDriverHuawei5, OfbDriverHuawei6])
def test_round2_driver_options(cls):
    d = cls("00:11:22:33:44:55")
    by_id = {h.handler_id: h for h in d.handlers}
    eq = by_id["config_eq"]
    # Preset list comes from the device, custom presets stay off.
    assert eq.w_options_predefined is False
    assert eq.w_custom is False
    assert eq.w_fake_built_in is False
    dc = by_id["dual_connect"]
    assert isinstance(dc, OfbHuaweiDualConnectNoUnpairHandler)
    assert dc.w_auto_connect is False


class _FakeDriver:
    def __init__(self):
        self.props = {}
        self.sent = []

    async def put_property(self, group, prop, value, extend_group=False):
        self.props.setdefault(group, {})[prop] = value

    async def send_package(self, pkg, timeout=5):
        self.sent.append(pkg)


def test_dual_connect_refuses_unpair():
    async def run():
        h = OfbHuaweiDualConnectNoUnpairHandler(w_auto_connect=False)
        h.driver = _FakeDriver()
        with pytest.raises(OfbNotSupportedError):
            await h.set_property("dual_connect", "001122334455:name", "")
        assert h.driver.sent == []
        await h._publish_capabilities()
        assert h.driver.props["dual_connect"]["unpair_supported"] == "false"

    asyncio.run(run())


@pytest.mark.parametrize("code,cls", [
    ("BTFT0020", OfbDriverHuawei6),
    ("BTFT0013", OfbDriverHuawei5),
    ("BTFT0018", OfbDriverHuaweiPro3),
    ("BTFT0006", OfbDriverHuaweiPro2),
    ("btft0020", OfbDriverHuawei6),
    (" BTFT0013 ", OfbDriverHuawei5),
])
def test_driver_for_model_code(code, cls):
    assert driver_for_model_code(code) is cls


def test_unknown_model_code():
    assert driver_for_model_code("NOPE") is None
    assert driver_for_model_code(None) is None
    assert driver_for_model_code("") is None


def test_dual_connect_refuses_auto_connect_when_off():
    async def run():
        h = OfbHuaweiDualConnectNoUnpairHandler(w_auto_connect=False)
        h.driver = _FakeDriver()
        for value in ("true", "false"):
            with pytest.raises(OfbNotSupportedError):
                await h.set_property("dual_connect", "001122334455:auto_connect", value)
        assert h.driver.sent == []

    asyncio.run(run())
