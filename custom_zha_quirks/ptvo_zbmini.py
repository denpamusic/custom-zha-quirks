"""Sonoff ZBMINI light with PTVO firmware quirk."""

from typing import Final

import zigpy.types as t
from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks import LocalDataCluster
from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
from zigpy.zcl.clusters.general import (
    AnalogInput,
    Basic,
    DeviceTemperature,
    GreenPowerProxy,
    MultistateInput,
    OnOff,
    OnOffConfiguration,
)

PTVO: Final = "PTVO"
CURRENT_TEMPERATURE: Final = 0x0055


class PtvoDeviceType(t.enum16):
    """Contains PTVO device types."""

    GENERIC = 0xFFFE


class DeviceTemperatureCluster(LocalDataCluster, DeviceTemperature):
    """PTVO device temperature cluster."""

    cluster_id = AnalogInput.cluster_id
    attributes = DeviceTemperature.attributes.copy()

    attributes.pop(0x0000)
    attributes.update(
        {
            CURRENT_TEMPERATURE: ("current_temperature", t.int16s, True),
        }
    )

    def _update_attribute(self, attrid, value):
        if attrid == CURRENT_TEMPERATURE:
            value *= 100

        super()._update_attribute(attrid, value)


class PtvoZbminiLightV1(CustomDevice):
    """PTVO ZBMINI light version 2."""

    signature = {
        MODELS_INFO: ((PTVO, "ZBMINI"),),
        ENDPOINTS: {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=61438
            # device_version=1
            # input_clusters=[0, 7]
            # output_clusters=[18]>
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: PtvoDeviceType.GENERIC,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    MultistateInput.cluster_id,
                ],
            },
            # <SimpleDescriptor endpoint=2 profile=260 device_type=61438
            # device_version=1
            # input_clusters=[6]
            # output_clusters=[6]>
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: PtvoDeviceType.GENERIC,
                INPUT_CLUSTERS: [
                    OnOff.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    OnOff.cluster_id,
                ],
            },
            # <SimpleDescriptor endpoint=3 profile=260 device_type=61438
            # device_version=1
            # input_clusters=[12]>
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: PtvoDeviceType.GENERIC,
                INPUT_CLUSTERS: [AnalogInput.cluster_id],
            },
            # <SimpleDescriptor endpoint=3 profile=41440 device_type=97
            # device_version=1
            # output_clusters=[33]>
            242: {
                PROFILE_ID: 41440,
                DEVICE_TYPE: 0x0061,
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    MultistateInput.cluster_id,
                ],
            },
            2: {
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    OnOff.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    OnOff.cluster_id,
                ],
            },
            3: {
                DEVICE_TYPE: zha.DeviceType.TEMPERATURE_SENSOR,
                INPUT_CLUSTERS: [DeviceTemperatureCluster],
            },
            242: {
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        }
    }


class PtvoZbminiLightV2(CustomDevice):
    """PTVO ZBMINI light version 2."""

    signature = {
        MODELS_INFO: ((PTVO, "ZBMINI"),),
        ENDPOINTS: {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=61438
            # device_version=1
            # input_clusters=[0, 7]
            # output_clusters=[0, 18]>
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: PtvoDeviceType.GENERIC,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    MultistateInput.cluster_id,
                ],
            },
            # <SimpleDescriptor endpoint=2 profile=260 device_type=61438
            # device_version=1
            # input_clusters=[6, 7]
            # output_clusters=[6]>
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: PtvoDeviceType.GENERIC,
                INPUT_CLUSTERS: [
                    OnOff.cluster_id,
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    OnOff.cluster_id,
                ],
            },
            # <SimpleDescriptor endpoint=3 profile=260 device_type=61438
            # device_version=1
            # input_clusters=[12]>
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: PtvoDeviceType.GENERIC,
                INPUT_CLUSTERS: [AnalogInput.cluster_id],
            },
            # <SimpleDescriptor endpoint=3 profile=41440 device_type=97
            # device_version=1
            # output_clusters=[33]>
            242: {
                PROFILE_ID: 41440,
                DEVICE_TYPE: 0x0061,
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    Basic.cluster_id,
                    MultistateInput.cluster_id,
                ],
            },
            2: {
                DEVICE_TYPE: zha.DeviceType.ON_OFF_LIGHT,
                INPUT_CLUSTERS: [
                    OnOff.cluster_id,
                    OnOffConfiguration.cluster_id,
                ],
                OUTPUT_CLUSTERS: [
                    OnOff.cluster_id,
                ],
            },
            3: {
                DEVICE_TYPE: zha.DeviceType.TEMPERATURE_SENSOR,
                INPUT_CLUSTERS: [DeviceTemperatureCluster],
            },
            242: {
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        }
    }
