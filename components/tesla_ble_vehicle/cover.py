import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import cover
from esphome.const import CONF_ID

from . import (
    CONF_TESLA_BLE_ID,
    TeslaBLEVehicle,
    TeslaChargePortDoorCover,
    TeslaFrunkCover,
    TeslaTrunkCover,
    TeslaWindowsCover,
)

DEPENDENCIES = ["tesla_ble_vehicle"]

CONF_TYPE = "type"

TYPES = {
    "trunk":            (TeslaTrunkCover,           "set_trunk_cover"),
    "frunk":            (TeslaFrunkCover,           "set_frunk_cover"),
    "windows":          (TeslaWindowsCover,         "set_windows_cover"),
    "charge_port_door": (TeslaChargePortDoorCover,  "set_charge_port_door_cover"),
}

CONFIG_SCHEMA = cv.typed_schema(
    {
        type_name: cover.cover_schema(cls).extend(
            {cv.GenerateID(CONF_TESLA_BLE_ID): cv.use_id(TeslaBLEVehicle)}
        )
        for type_name, (cls, _) in TYPES.items()
    },
    key=CONF_TYPE,
    lower=True,
)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_TESLA_BLE_ID])
    var = cg.new_Pvariable(config[CONF_ID])
    await cover.register_cover(var, config)
    cg.add(var.set_parent(parent))
    cg.add(getattr(parent, TYPES[config[CONF_TYPE]][1])(var))
