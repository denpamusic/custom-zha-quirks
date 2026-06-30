"""Custom quirk for Aqara LED Bulb T1.

Adds power outage memory.
"""

from zigpy.quirks.v2 import QuirkBuilder
from zhaquirks.xiaomi.aqara.light_acn import OppleClusterLight

from zhaquirks.xiaomi import AQARA

(
    QuirkBuilder(AQARA, "lumi.light.acn014")
    .replaces(OppleClusterLight, endpoint_id=1)
    .switch(
        OppleClusterLight.AttributeDefs.power_outage_memory.name,
        OppleClusterLight.cluster_id,
        translation_key="power_outage_memory",
        fallback_name="Power outage memory",
    )
    .add_to_registry()
)
