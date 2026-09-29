from openfreebuds.driver.huawei.handler.config_equalizer import OfbHuaweiEqualizerPresetHandler
from openfreebuds.exceptions import OfbNotSupportedError


class OfbHuaweiEqualizerBuiltInOnlyHandler(OfbHuaweiEqualizerPresetHandler):
    """
    Equalizer handler that only switches between built-in presets (LibreBuds).

    When custom presets are off, writes to the custom equalizer rows and the
    saved flag are refused before anything is sent, because the 2B/49 custom
    preset write was not confirmed on real earbuds. Preset selection works as
    in the upstream handler. Other models keep the upstream handler unchanged.
    """

    async def set_property(self, group: str, prop: str, value):
        if not self.w_custom and prop in ("equalizer_rows", "equalizer_saved"):
            raise OfbNotSupportedError("Custom equalizer presets are not supported for this device")
        return await super().set_property(group, prop, value)
