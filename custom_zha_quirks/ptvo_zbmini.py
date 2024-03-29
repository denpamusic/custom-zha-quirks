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
from zigpy.quirks import CustomDevice, CustomCluster
from zigpy.zcl.clusters.general import (
    AnalogInput,
    Basic,
    DeviceTemperature,
    GreenPowerProxy,
    MultistateInput,
    OnOff,
    OnOffConfiguration,
)
from zigpy.zcl.clusters.measurement import TemperatureMeasurement

PTVO: Final = "PTVO"

PRESENT_VALUE: Final = 0x0055
CURRENT_TEMPERATURE: Final = 0x0000


class PtvoDeviceType(t.enum16):
    """Contains PTVO device types."""

    GENERIC = 0xFFFE


class AnalogInputCluster(CustomCluster, AnalogInput):
    """PTVO device temperature analog input cluster."""

    def _update_attribute(self, attrid, value):
        super()._update_attribute(attrid, value)

        if attrid == PRESENT_VALUE:
            self.endpoint.device_temperature.update_attribute(
                CURRENT_TEMPERATURE, value * 100
            )


class DeviceTemperatureCluster(LocalDataCluster, DeviceTemperature):
    """PTVO device temperature cluster."""


class PtvoZbminiLightV1(CustomDevice):
    """PTVO ZBMINI light version 1."""

    signature = {
        MODELS_INFO: ((PTVO, "ZBMINI"),),
        ENDPOINTS: {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=65534
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
            # <SimpleDescriptor endpoint=2 profile=260 device_type=65534
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
            # <SimpleDescriptor endpoint=3 profile=260 device_type=65534
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
                INPUT_CLUSTERS: [
                    AnalogInputCluster,
                    DeviceTemperatureCluster,
                ],
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
            # <SimpleDescriptor endpoint=1 profile=260 device_type=65534
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
            # <SimpleDescriptor endpoint=2 profile=260 device_type=65534
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
            # <SimpleDescriptor endpoint=3 profile=260 device_type=65534
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
                INPUT_CLUSTERS: [
                    AnalogInputCluster,
                    DeviceTemperatureCluster,
                ],
            },
            242: {
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        }
    }


class PtvoZbminiLightV3(CustomDevice):
    """PTVO ZBMINI light version 3."""

    signature = {
        MODELS_INFO: ((PTVO, "ZBMINI"),),
        ENDPOINTS: {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=65534
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
            # <SimpleDescriptor endpoint=2 profile=260 device_type=65534
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
            # <SimpleDescriptor endpoint=3 profile=260 device_type=65534
            # device_version=1
            # input_clusters=[1026]>
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: PtvoDeviceType.GENERIC,
                INPUT_CLUSTERS: [TemperatureMeasurement.cluster_id],
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
                INPUT_CLUSTERS: [TemperatureMeasurement.cluster_id],
            },
            242: {
                OUTPUT_CLUSTERS: [GreenPowerProxy.cluster_id],
            },
        }
    }


class PtvoZbminiLightV3EndDevice(CustomDevice):
    """PTVO ZBMINI light version 3 (end device version)."""

    signature = {
        MODELS_INFO: ((PTVO, "ZBMINI"),),
        ENDPOINTS: {
            # <SimpleDescriptor endpoint=1 profile=260 device_type=65534
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
            # <SimpleDescriptor endpoint=2 profile=260 device_type=65534
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
            # <SimpleDescriptor endpoint=3 profile=260 device_type=65534
            # device_version=1
            # input_clusters=[1026]>
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: PtvoDeviceType.GENERIC,
                INPUT_CLUSTERS: [TemperatureMeasurement.cluster_id],
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
                INPUT_CLUSTERS: [TemperatureMeasurement.cluster_id],
            },
        }
    }
