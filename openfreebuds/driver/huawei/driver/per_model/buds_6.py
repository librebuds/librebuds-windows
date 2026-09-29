from openfreebuds.driver.huawei.driver.generic import OfbDriverHuaweiGeneric
from openfreebuds.driver.huawei.handler import *


class OfbDriverHuawei6(OfbDriverHuaweiGeneric):
    """
    HUAWEI FreeBuds 6 (LibreBuds).

    A handler is enabled only when every command it reads returned data on
    real earbuds in LibreBuds test rounds 1 and 2 (FreeBuds 6, FreeBuds 5,
    FreeBuds Pro 3).

    Confirmed and enabled:
    - device info (01/07), battery (01/08), noise control (2B/2A, write 2B/04)
    - double tap (01/20), triple tap (01/26)
    - long press (2B/17) and noise-control cycle (2B/19)
    - swipe for volume (2B/1F)
    - wear detection, auto pause (2B/11)
    - equalizer (2B/4A). The preset list is taken from the device, because the
      ids differ per model (FreeBuds 6 reported presets 0, 2, 3, 9, 11 and 12). Only switching between built-in presets is
      offered; custom presets are off and custom equalizer writes are
      refused before anything is sent.
    - multipoint toggle and host list (2B/2F, 2B/31) with connect and
      disconnect (2B/33). Unpairing a host is refused and hidden in the UI.
      The auto-connect flag is off because round 2 did not confirm that the
      host list carries it.

    Excluded:
    - low latency: 2B/6C returned an error
    - in-ear state: relies on 2B/03 pushes, and 2B/03 returned an error
    - voice language: the handler also writes the language (0C/01), which is
      never sent; the read (0C/02) alone gives the user nothing to act on
    - sound quality preference: 2B/A3 read returned data, but the write is
      unconfirmed
    - pinch gestures: 2B/21 returned an error
    """
    def __init__(self, address):
        super().__init__(address)
        # SPEC-GAP: RFCOMM channel not confirmed for this model; channel 1 matches FreeBuds 6i and Pro 3.
        self._spp_service_port = 1
        self.handlers = [
            OfbHuaweiInfoHandler(),
            OfbHuaweiBatteryHandler(),
            OfbHuaweiAncHandler(w_cancel_lvl=True, w_cancel_dynamic=True),
            OfbHuaweiActionDoubleTapHandler(w_in_call=True),
            OfbHuaweiActionTripleTapHandler(),
            OfbHuaweiActionLongTapSplitHandler(w_right=True),
            OfbHuaweiActionSwipeGestureHandler(),
            OfbHuaweiConfigAutoPauseHandler(),
            OfbHuaweiEqualizerBuiltInOnlyHandler(),
            OfbHuaweiDualConnectNoUnpairHandler(w_auto_connect=False),
        ]
