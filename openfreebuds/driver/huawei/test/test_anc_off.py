"""
Round 2 hardware tests confirmed the earbuds accept FF as "choose the level",
including for off, so upstream's write is kept as is.
"""
import pytest

from openfreebuds.driver.huawei.driver.debug import FbDriverHuaweiGenericFixture
from openfreebuds.driver.huawei.handler import OfbHuaweiAncHandler
from openfreebuds.driver.huawei.package import HuaweiSppPackage


def fixture(extra_model=None):
    read = HuaweiSppPackage.read_rq(b"\x2b\x2a", [1, 2])
    state_cancel = HuaweiSppPackage(b"\x2b\x2a", [(1, b"\x03\x01")])
    ack = HuaweiSppPackage(b"\x2b\x04", [(2, b"\x00")])
    model = {
        read.to_bytes(): [state_cancel.to_bytes()],
        HuaweiSppPackage.change_rq(b"\x2b\x04", [(1, b"\x00\xff")]).to_bytes(): [ack.to_bytes()],
        HuaweiSppPackage.change_rq(b"\x2b\x04", [(1, b"\x01\xff")]).to_bytes(): [ack.to_bytes()],
    }
    model.update(extra_model or {})
    return FbDriverHuaweiGenericFixture(
        handlers=[OfbHuaweiAncHandler(w_cancel_lvl=True, w_cancel_dynamic=True)],
        package_response_model=model,
    )


@pytest.mark.asyncio
async def test_mode_off_sends_ff_level_marker():
    driver = fixture()
    await driver.start()
    await driver.set_property("anc", "mode", "normal")
    expected = HuaweiSppPackage.change_rq(b"\x2b\x04", [(1, b"\x00\xff")]).to_bytes()
    assert ("send", expected) in driver.package_log


@pytest.mark.asyncio
async def test_mode_cancellation_keeps_level_marker():
    driver = fixture()
    await driver.start()
    await driver.set_property("anc", "mode", "cancellation")
    expected = HuaweiSppPackage.change_rq(b"\x2b\x04", [(1, b"\x01\xff")]).to_bytes()
    assert ("send", expected) in driver.package_log
