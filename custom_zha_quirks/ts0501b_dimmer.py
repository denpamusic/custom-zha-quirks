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
    """Custom LevelControl cluster to fix level update and range."""

    CURRENT_LEVEL_ATTR = LevelControl.AttributeDefs.current_level.id

    async def _update_current_level(
        self, level: int, manufacturer: int | None = None
    ) -> None:
        """Update current level."""
        previous_level = self._attr_cache.get(self.CURRENT_LEVEL_ATTR)
        if level != previous_level:
            await self.write_attributes(
                {self.CURRENT_LEVEL_ATTR: level}, manufacturer=manufacturer
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
        """Override command method to update current_level on move_to_level."""
        if command_id in (
            self.ServerCommandDefs.move_to_level.id,
            self.ServerCommandDefs.move_to_level_with_on_off.id,
        ):
            if kwargs and "level" in kwargs:
                level = kwargs["level"]
            elif args:
                level = args[0]
            else:
                level = 0

            await self._update_current_level(level, manufacturer=manufacturer)
            # convert dim level to brightness [30...254]
            brightness = level * (254 - 30) // 254 + 30
            if args:
                args = list(args)
                args[0] = brightness
            else:
                kwargs["level"] = brightness

        return await super().command(
            command_id,
            *args,
            manufacturer=manufacturer,
            expect_reply=expect_reply,
            tsn=tsn,
            **kwargs,
        )


class DimmerModule(CustomDevice):
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
