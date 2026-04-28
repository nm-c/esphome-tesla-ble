import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import switch

from . import (
    CONF_TESLA_BLE_ID,
    TeslaBLEVehicle,
    TeslaChargingSwitch,
    TeslaSentryModeSwitch,
    TeslaSteeringWheelHeatSwitch,
)

DEPENDENCIES = ["tesla_ble_vehicle"]

CONF_TYPE = "type"

TYPES = {
    "charging":            (TeslaChargingSwitch,           "set_charging_switch"),
    "steering_wheel_heat": (TeslaSteeringWheelHeatSwitch,  "set_steering_wheel_heat_switch"),
    "sentry_mode":         (TeslaSentryModeSwitch,         "set_sentry_mode_switch"),
}

CONFIG_SCHEMA = cv.typed_schema(
    {
        type_name: switch.switch_schema(cls).extend(
            {cv.GenerateID(CONF_TESLA_BLE_ID): cv.use_id(TeslaBLEVehicle)}
        )
        for type_name, (cls, _) in TYPES.items()
    },
    key=CONF_TYPE,
    lower=True,
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_TESLA_BLE_ID])
    var = await switch.new_switch(config)
    cg.add(var.set_parent(parent))
    cg.add(getattr(parent, TYPES[config[CONF_TYPE]][1])(var))
