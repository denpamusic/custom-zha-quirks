"""Sonoff ZBMicro - USB Zigbee Switch."""

from zigpy.quirks import CustomCluster
from zigpy.quirks.v2 import QuirkBuilder
import zigpy.types as t
from zigpy.zcl.foundation import BaseAttributeDefs, ZCLAttributeDef

SHENZHEN_COOLKIT_TECHNOLOGY_CO_LTD_MANUFACTURER_ID = 0x1286


class SonoffCluster(CustomCluster):
    """Custom Sonoff cluster."""

    cluster_id = 0xFC11

    manufacturer_id_override = SHENZHEN_COOLKIT_TECHNOLOGY_CO_LTD_MANUFACTURER_ID

    class AttributeDefs(BaseAttributeDefs):
        """Attribute definitions."""

        turbo_mode = ZCLAttributeDef(
            id=0x0012,
            type=t.int16s,
            is_manufacturer_specific=True,
        )


(
    QuirkBuilder("SONOFF", "ZBMicro")
    .replaces(SonoffCluster)
    .switch(
        SonoffCluster.AttributeDefs.turbo_mode.name,
        SonoffCluster.cluster_id,
        off_value=9,
        on_value=20,
        translation_key="turbo_mode",
        fallback_name="Turbo mode",
    )
    .add_to_registry()
)
