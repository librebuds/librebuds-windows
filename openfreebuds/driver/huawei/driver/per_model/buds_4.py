from openfreebuds.driver.huawei.driver.generic import OfbDriverHuaweiGeneric
from openfreebuds.driver.huawei.handler import *


class OfbDriverHuawei4(OfbDriverHuaweiGeneric):
    """
    HUAWEI FreeBuds 4 (LibreBuds, experimental: not tested on hardware).

    Only device info, battery and noise control are enabled. These are the
    features confirmed on FreeBuds 5 and FreeBuds 6; nothing else is added
    until a FreeBuds 4 has been tested.
    """
    def __init__(self, address):
        super().__init__(address)
        # SPEC-GAP: RFCOMM channel not confirmed for this model; channel 1 matches FreeBuds 6i and Pro 3.
        self._spp_service_port = 1
        self.handlers = [
            OfbHuaweiInfoHandler(),
            OfbHuaweiBatteryHandler(),
            OfbHuaweiAncHandler(w_cancel_lvl=True, w_cancel_dynamic=True),
        ]
