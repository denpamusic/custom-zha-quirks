"""GIRIER 0/1-10V dimmer module single channel."""

from typing import Any
from zigpy.profiles import zgp, zha
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import (
    Basic,
    GreenPowerProxy,
    Groups,
    LevelControl,
    OnOff,
    Ota,
    Scenes,
    Time,
)
from zigpy.zcl.clusters.lighting import Color

from zigpy.zcl import foundation
from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.tuya import TuyaManufCluster
from zhaquirks import CustomCluster


class TuyaLevelControl(CustomCluster, LevelControl):
    """Custom LevelControl cluster to fix level update and on/off."""

    @staticmethod
    def on_off_command_id(on_off: bool) -> int:
        """Get command id for boolean value."""
        return (
            OnOff.commands_by_name["on"].id
            if on_off
            else OnOff.commands_by_name["off"].id
        )

    async def command(
        self,
        command_id: int,
        *args,
        manufacturer: int | None = None,
        expect_reply: bool = True,
        tsn: int | None = None,
        **kwargs: Any,
    ):
        """Override command method to update current_level on move_to_level(_with_on_off)."""
        if kwargs and "level" in kwargs:
            level = kwargs["level"]
        elif args:
            level = args[0]
        else:
            level = 0

        on_off = bool(level)

        if (
            command_id == self.commands_by_name["move_to_level_with_on_off"].id
            and self.endpoint.on_off.get("on_off") != on_off
        ):
            self.create_catching_task(
                self.endpoint.on_off.command(
                    command_id=self.on_off_command_id(on_off),
                    manufacturer=manufacturer,
                    expect_reply=False,
                )
            )

        if (
            command_id == self.commands_by_name["move_to_level_with_on_off"].id
            and not on_off
        ):
            return foundation.GENERAL_COMMANDS[
                foundation.GeneralCommand.Default_Response
            ].schema(command_id=command_id, status=foundation.Status.SUCCESS)

        if command_id in (
            self.commands_by_name["move_to_level"].id,
            self.commands_by_name["move_to_level_with_on_off"].id,
        ):
            await self.write_attributes(
                {self.attributes_by_name["current_level"].id: level},
                manufacturer=manufacturer,
            )

        return await super().command(
            command_id,
            *args,
            manufacturer=manufacturer,
            expect_reply=expect_reply,
            tsn=tsn,
            **kwargs,
        )


class DimmerModule0_10V(CustomDevice):
    """GIRIER 0/1-10V dimmer module single channel."""

    signature = {
        MODELS_INFO: [
            ("_TZ3218_ofguu6mz", "TS0501B"),
        ],
        ENDPOINTS: {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=257
            # input_clusters=[0, 3, 5, 6, 8, 768, 61184]
            # output_clusters=[10, 25]>
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.DIMMABLE_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    LevelControl.cluster_id,
                    Color.cluster_id,
                    TuyaManufCluster.cluster_id,
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id],
            },
            242: {
                # <SimpleDescriptor endpoint=242 profile=41440 device_type=97
                # input_clusters=[]
                # output_clusters=[33]
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }
    replacement = {
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.DIMMABLE_LIGHT,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    TuyaLevelControl,
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id],
            },
            242: {
                PROFILE_ID: zgp.PROFILE_ID,
                DEVICE_TYPE: zgp.DeviceType.PROXY_BASIC,
                INPUT_CLUSTERS: [],
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }
