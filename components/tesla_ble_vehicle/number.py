import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import number
from esphome.const import CONF_ID, CONF_MAX_VALUE, CONF_MIN_VALUE, CONF_STEP
from esphome.core import CORE

from . import (
    CONF_CHARGING_AMPS_MAX,
    CONF_TESLA_BLE_ID,
    TeslaBLEVehicle,
    TeslaChargingAmpsNumber,
    TeslaChargingLimitNumber,
)

DEPENDENCIES = ["tesla_ble_vehicle"]

CONF_TYPE = "type"

# type → (class, setter, default_min, default_max, default_step).
# default_max=None means: take from the parent component's `charging_amps_max:`.
TYPES = {
    "charging_amps":  (TeslaChargingAmpsNumber,  "set_charging_amps_number",  0,  None, 1),
    "charging_limit": (TeslaChargingLimitNumber, "set_charging_limit_number", 50, 100,  1),
}


def _per_type_schema(cls, default_min, default_max, default_step):
    schema = number.number_schema(cls).extend(
        {
            cv.GenerateID(CONF_TESLA_BLE_ID): cv.use_id(TeslaBLEVehicle),
            cv.Optional(CONF_MIN_VALUE, default=default_min): cv.float_,
            cv.Optional(CONF_STEP, default=default_step): cv.positive_float,
        }
    )
    if default_max is None:
        return schema.extend({cv.Optional(CONF_MAX_VALUE): cv.float_})
    return schema.extend(
        {cv.Optional(CONF_MAX_VALUE, default=default_max): cv.float_}
    )


CONFIG_SCHEMA = cv.typed_schema(
    {
        type_name: _per_type_schema(cls, default_min, default_max, default_step)
        for type_name, (cls, _, default_min, default_max, default_step) in TYPES.items()
    },
    key=CONF_TYPE,
    lower=True,
)


def _resolve_max_from_parent(parent_id):
    parent_conf = CORE.config["tesla_ble_vehicle"]
    if isinstance(parent_conf, list):
        for c in parent_conf:
            if c[CONF_ID] == parent_id:
                return c.get(CONF_CHARGING_AMPS_MAX, 32)
        return 32
    return parent_conf.get(CONF_CHARGING_AMPS_MAX, 32)


async def to_code(config):
    parent = await cg.get_variable(config[CONF_TESLA_BLE_ID])
    cls, setter, _, _, _ = TYPES[config[CONF_TYPE]]

    max_value = config.get(CONF_MAX_VALUE)
    if max_value is None:
        max_value = _resolve_max_from_parent(config[CONF_TESLA_BLE_ID])

    var = await number.new_number(
        config,
        min_value=config[CONF_MIN_VALUE],
        max_value=max_value,
        step=config[CONF_STEP],
    )
    cg.add(var.set_parent(parent))
    cg.add(getattr(parent, setter)(var))
