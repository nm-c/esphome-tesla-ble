import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import button

from . import (
    CONF_TESLA_BLE_ID,
    TeslaBLEVehicle,
    TeslaFlashLightsButton,
    TeslaForceUpdateButton,
    TeslaHonkHornButton,
    TeslaPairButton,
    TeslaRegenerateKeyButton,
    TeslaUnlatchDriverDoorButton,
    TeslaWakeButton,
)

DEPENDENCIES = ["tesla_ble_vehicle"]

CONF_TYPE = "type"

# type → (c++ subclass for declare_id, parent setter or None for self-contained press handlers)
TYPES = {
    "wake":                (TeslaWakeButton,              "set_wake_button"),
    "pair":                (TeslaPairButton,              "set_pair_button"),
    "regenerate_key":      (TeslaRegenerateKeyButton,     "set_regenerate_key_button"),
    "force_update":        (TeslaForceUpdateButton,       "set_force_update_button"),
    "unlatch_driver_door": (TeslaUnlatchDriverDoorButton, None),
    "flash_lights":        (TeslaFlashLightsButton,       None),
    "honk_horn":           (TeslaHonkHornButton,          None),
}

CONFIG_SCHEMA = cv.typed_schema(
    {
        type_name: button.button_schema(cls).extend(
            {cv.GenerateID(CONF_TESLA_BLE_ID): cv.use_id(TeslaBLEVehicle)}
        )
        for type_name, (cls, _) in TYPES.items()
    },
    key=CONF_TYPE,
    lower=True,
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_TESLA_BLE_ID])
    var = await button.new_button(config)
    cg.add(var.set_parent(parent))
    setter = TYPES[config[CONF_TYPE]][1]
    if setter is not None:
        cg.add(getattr(parent, setter)(var))
