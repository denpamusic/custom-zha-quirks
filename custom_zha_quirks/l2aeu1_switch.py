"""Custom quirk for Aqara H1 Double Rocker Switch (no neutral) with decoupled mode entity.

Adds operation_mode select entities and button event support.
"""

from zigpy.profiles import zha
from zigpy.quirks.v2 import QuirkBuilder, EntityType


from zhaquirks.xiaomi import LUMI
from zhaquirks.xiaomi.aqara.opple_switch import (
    OppleOperationMode,
    OppleIndicatorLight,
    OppleSwitchCluster,
    XiaomiOpple2ButtonSwitchBase,
)
from zhaquirks.xiaomi.aqara.opple_remote import MultistateInputCluster

(
    QuirkBuilder(LUMI, "lumi.switch.l2aeu1")
    # Replace with OppleSwitchCluster on main endpoints
    .replaces(OppleSwitchCluster, endpoint_id=1)
    .replaces(OppleSwitchCluster, endpoint_id=2)
    # Add button event endpoints (these don't exist in the device signature)
    .adds_endpoint(41, device_type=zha.DeviceType.ON_OFF_LIGHT_SWITCH)
    .adds_endpoint(42, device_type=zha.DeviceType.ON_OFF_LIGHT_SWITCH)
    .adds_endpoint(51, device_type=zha.DeviceType.ON_OFF_LIGHT_SWITCH)
    # Add MultistateInputCluster to button endpoints
    .adds(MultistateInputCluster, endpoint_id=41)
    .adds(MultistateInputCluster, endpoint_id=42)
    .adds(MultistateInputCluster, endpoint_id=51)
    # Endpoint 1 - Button 1 operation mode
    .enum(
        attribute_name="operation_mode",
        enum_class=OppleOperationMode,
        cluster_id=0xFCC0,
        endpoint_id=1,
        entity_type=EntityType.CONFIG,
        translation_key="operation_mode",
        fallback_name="Operation Mode (Button 1)",
    )
    # Endpoint 2 - Button 2 operation mode
    .enum(
        attribute_name="operation_mode",
        enum_class=OppleOperationMode,
        cluster_id=0xFCC0,
        endpoint_id=2,
        entity_type=EntityType.CONFIG,
        translation_key="operation_mode_2",
        fallback_name="Operation Mode (Button 2)",
    )
    # Indicator light direction
    .enum(
        attribute_name="reverse_indicator_light",
        enum_class=OppleIndicatorLight,
        cluster_id=0xFCC0,
        endpoint_id=1,
        entity_type=EntityType.CONFIG,
        translation_key="indicator_light",
        fallback_name="Indicator Light Mode",
    )
    # Add device automation triggers for button events
    .device_automation_triggers(XiaomiOpple2ButtonSwitchBase.device_automation_triggers)
    .add_to_registry()
)
