from openfreebuds.driver.huawei.handler.dual_connect.handler import OfbHuaweiDualConnectHandler
from openfreebuds.exceptions import OfbNotSupportedError


class OfbHuaweiDualConnectNoUnpairHandler(OfbHuaweiDualConnectHandler):
    """
    Multipoint handler that never sends the unpair action (LibreBuds).

    Unpairing a host was not confirmed on real earbuds, so the request is
    refused here and the "unpair_supported" flag tells the UI to hide the
    button. Other models keep the upstream handler unchanged.
    """

    async def on_init(self):
        await self._publish_capabilities()
        await super().on_init()

    async def _publish_capabilities(self):
        await self.driver.put_property("dual_connect", "unpair_supported", "false")

    async def set_property(self, group: str, payload: str, value: str):
        _, prop, *_ = *payload.split(":"), "", ""
        if prop == "name" and value == "":
            raise OfbNotSupportedError("Unpairing a multipoint host is not supported for this device")
        return await super().set_property(group, payload, value)
