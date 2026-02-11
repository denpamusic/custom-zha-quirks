"""Custom quirk for Aqara H1 Double Rocker Switch (no neutral) with decoupled mode entity.

Adds operation_mode select entities and button event support.
"""

from zigpy.profiles import zha
from zigpy.quirks.v2 import QuirkBuilder, EntityType

from zhaquirks.const import (
    ARGS,
    ATTR_ID,
    BUTTON,
    BUTTON_1,
    BUTTON_2,
    CLUSTER_ID,
    COMMAND,
    COMMAND_BUTTON_DOUBLE,
    COMMAND_BUTTON_HOLD,
    COMMAND_BUTTON_SINGLE,
    COMMAND_DOUBLE,
    COMMAND_SINGLE,
    ENDPOINT_ID,
    PRESS_TYPE,
    VALUE,
)
from zhaquirks.xiaomi import LUMI
from zhaquirks.xiaomi.aqara.opple_switch import (
    BOTH_BUTTONS,
    OppleOperationMode,
    OppleIndicatorLight,
    OppleSwitchCluster,
)
from zhaquirks.xiaomi.aqara.opple_remote import MultistateInputCluster


# Device automation trigger definitions matching XiaomiOpple2ButtonSwitchBase exactly
DEVICE_AUTOMATION_TRIGGERS = {
    # Button 1 (left) - endpoint 41
    (COMMAND_BUTTON_SINGLE, BUTTON_1): {
        ENDPOINT_ID: 41,
        CLUSTER_ID: 18,
        COMMAND: "41_single",
        ARGS: {ATTR_ID: 0x0055, PRESS_TYPE: COMMAND_SINGLE, VALUE: 1},
    },
    (COMMAND_BUTTON_DOUBLE, BUTTON_1): {
        ENDPOINT_ID: 41,
        CLUSTER_ID: 18,
        COMMAND: "41_double",
        ARGS: {ATTR_ID: 0x0055, PRESS_TYPE: COMMAND_DOUBLE, VALUE: 2},
    },
    # Button 2 (right) - endpoint 42
    (COMMAND_BUTTON_SINGLE, BUTTON_2): {
        ENDPOINT_ID: 42,
        CLUSTER_ID: 18,
        COMMAND: "42_single",
        ARGS: {ATTR_ID: 0x0055, PRESS_TYPE: COMMAND_SINGLE, VALUE: 1},
    },
    (COMMAND_BUTTON_DOUBLE, BUTTON_2): {
        ENDPOINT_ID: 42,
        CLUSTER_ID: 18,
        COMMAND: "42_double",
        ARGS: {ATTR_ID: 0x0055, PRESS_TYPE: COMMAND_DOUBLE, VALUE: 2},
    },
    # Both buttons - endpoint 51
    (COMMAND_BUTTON_SINGLE, BOTH_BUTTONS): {
        ENDPOINT_ID: 51,
        CLUSTER_ID: 18,
        COMMAND: "51_single",
        ARGS: {ATTR_ID: 0x0055, PRESS_TYPE: COMMAND_SINGLE, VALUE: 1},
    },
    (COMMAND_BUTTON_DOUBLE, BOTH_BUTTONS): {
        ENDPOINT_ID: 51,
        CLUSTER_ID: 18,
        COMMAND: "51_double",
        ARGS: {ATTR_ID: 0x0055, PRESS_TYPE: COMMAND_DOUBLE, VALUE: 2},
    },
    # Hold events come from cluster 0xFCC0 on endpoint 1
    (COMMAND_BUTTON_HOLD, BUTTON): {
        ENDPOINT_ID: 1,
        CLUSTER_ID: 0xFCC0,
        ARGS: {ATTR_ID: 0x00FC, VALUE: 0},
    },
}

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
    .device_automation_triggers(DEVICE_AUTOMATION_TRIGGERS)
    .add_to_registry()
)
