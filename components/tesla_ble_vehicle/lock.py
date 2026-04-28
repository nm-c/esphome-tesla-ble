import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import lock
from esphome.const import CONF_ID

from . import (
    CONF_TESLA_BLE_ID,
    TeslaBLEVehicle,
    TeslaChargePortLatchLock,
    TeslaDoorsLock,
)

DEPENDENCIES = ["tesla_ble_vehicle"]

CONF_TYPE = "type"

TYPES = {
    "doors":             (TeslaDoorsLock,           "set_doors_lock"),
    "charge_port_latch": (TeslaChargePortLatchLock, "set_charge_port_latch_lock"),
}

CONFIG_SCHEMA = cv.typed_schema(
    {
        type_name: lock.lock_schema(cls).extend(
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
    await lock.register_lock(var, config)
    cg.add(var.set_parent(parent))
    cg.add(getattr(parent, TYPES[config[CONF_TYPE]][1])(var))
