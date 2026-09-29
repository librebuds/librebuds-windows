"""Model codes reported in device info (TLV 15, stored as info/device_model) mapped to drivers.

Source: LibreBuds live test rounds 1 and 2. Extend as new models are confirmed.
"""
from openfreebuds.driver.huawei.driver.per_model import (
    OfbDriverHuawei5,
    OfbDriverHuawei6,
    OfbDriverHuaweiPro2,
    OfbDriverHuaweiPro3,
)

MODEL_CODE_TO_DRIVER = {
    "BTFT0013": OfbDriverHuawei5,
    "BTFT0020": OfbDriverHuawei6,
    "BTFT0018": OfbDriverHuaweiPro3,
    "BTFT0006": OfbDriverHuaweiPro2,
}


def driver_for_model_code(code):
    if not code or not isinstance(code, str):
        return None
    return MODEL_CODE_TO_DRIVER.get(code.strip().upper())
