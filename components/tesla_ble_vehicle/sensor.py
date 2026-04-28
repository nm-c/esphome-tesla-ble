import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor

from . import CONF_TESLA_BLE_ID, TeslaBLEVehicle

DEPENDENCIES = ["tesla_ble_vehicle"]

CONF_TYPE = "type"

# yaml `type:` value → c++ id string passed to TeslaBLEVehicle::set_sensor.
# Must stay in sync with vehicle_state_manager.cpp.
TYPES = [
    "battery_level",
    "range",
    "charger_power",
    "charger_voltage",
    "charger_current",
    "charging_rate",
    "energy_added",
    "time_to_full",
    "outside_temp",
    "odometer",
    "tpms_front_left",
    "tpms_front_right",
    "tpms_rear_left",
    "tpms_rear_right",
]

CONFIG_SCHEMA = sensor.sensor_schema().extend(
    {
        cv.GenerateID(CONF_TESLA_BLE_ID): cv.use_id(TeslaBLEVehicle),
        cv.Required(CONF_TYPE): cv.one_of(*TYPES, lower=True),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_TESLA_BLE_ID])
    var = await sensor.new_sensor(config)
    cg.add(parent.set_sensor(config[CONF_TYPE], var))
