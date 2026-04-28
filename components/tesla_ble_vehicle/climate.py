import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate
from esphome.const import CONF_ID

from . import CONF_TESLA_BLE_ID, TeslaBLEVehicle, TeslaClimate

DEPENDENCIES = ["tesla_ble_vehicle"]

CONFIG_SCHEMA = climate.climate_schema(TeslaClimate).extend(
    {
        cv.GenerateID(CONF_TESLA_BLE_ID): cv.use_id(TeslaBLEVehicle),
    }
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_TESLA_BLE_ID])
    var = cg.new_Pvariable(config[CONF_ID])
    await climate.register_climate(var, config)
    cg.add(var.set_parent(parent))
    cg.add(parent.set_climate(var))
