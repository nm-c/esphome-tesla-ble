import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor

from . import CONF_TESLA_BLE_ID, TeslaBLEVehicle

DEPENDENCIES = ["tesla_ble_vehicle"]

CONF_TYPE = "type"

# yaml `type:` value → c++ id string passed to TeslaBLEVehicle::set_text_sensor.
TYPES = [
    "charging_state",
    "iec61851_state",
    "shift_state",
]

CONFIG_SCHEMA = text_sensor.text_sensor_schema().extend(
    {
        cv.GenerateID(CONF_TESLA_BLE_ID): cv.use_id(TeslaBLEVehicle),
        cv.Required(CONF_TYPE): cv.one_of(*TYPES, lower=True),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_TESLA_BLE_ID])
    var = await text_sensor.new_text_sensor(config)
    cg.add(parent.set_text_sensor(config[CONF_TYPE], var))
