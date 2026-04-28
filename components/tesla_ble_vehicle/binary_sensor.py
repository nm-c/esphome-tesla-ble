import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor

from . import CONF_TESLA_BLE_ID, TeslaBLEVehicle

DEPENDENCIES = ["tesla_ble_vehicle"]

CONF_TYPE = "type"

# yaml `type:` value → c++ id string passed to TeslaBLEVehicle::set_binary_sensor.
# Must stay in sync with the ids vehicle_state_manager.cpp publishes to.
TYPES = [
    "asleep",
    "user_present",
    "charger",
    "parking_brake",
    "door_driver_front",
    "door_driver_rear",
    "door_passenger_front",
    "door_passenger_rear",
    "window_driver_front",
    "window_driver_rear",
    "window_passenger_front",
    "window_passenger_rear",
    "sunroof",
]

CONFIG_SCHEMA = binary_sensor.binary_sensor_schema().extend(
    {
        cv.GenerateID(CONF_TESLA_BLE_ID): cv.use_id(TeslaBLEVehicle),
        cv.Required(CONF_TYPE): cv.one_of(*TYPES, lower=True),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_TESLA_BLE_ID])
    var = await binary_sensor.new_binary_sensor(config)
    cg.add(parent.set_binary_sensor(config[CONF_TYPE], var))
