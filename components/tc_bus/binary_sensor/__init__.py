import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import binary_sensor
from esphome.const import CONF_ID, CONF_ICON, CONF_TYPE
from .. import tc_bus_ns, TCBusComponent, CONF_TC_ID, COMMAND_TYPES

CommandListenerBinarySensor = tc_bus_ns.class_("CommandListenerBinarySensor", binary_sensor.BinarySensor, cg.Component)

CONF_ADDRESS = "address"
CONF_ADDRESS_LAMBDA = "address_lambda"

CONF_PAYLOAD = "payload"
CONF_PAYLOAD_LAMBDA = "payload_lambda"

CONF_COMMAND = "command"
CONF_COMMAND_LAMBDA = "command_lambda"
CONF_COMMAND_LAMBDA_LEGACY = "lambda"

CONF_SERIAL_NUMBER = "serial_number"

CONF_NAME = "name"
CONF_AUTO_OFF = "auto_off"

DEPENDENCIES = ["tc_bus"]

def validate(config):
    config = config.copy()

    has_command_option = any(
        key in config for key in [CONF_COMMAND, CONF_COMMAND_LAMBDA, CONF_COMMAND_LAMBDA_LEGACY]
    )

    has_type_option = CONF_TYPE in config

    has_address_option = any(
        key in config for key in [CONF_ADDRESS, CONF_ADDRESS_LAMBDA]
    )

    has_payload_option = any(
        key in config for key in [CONF_PAYLOAD, CONF_PAYLOAD_LAMBDA]
    )

    has_serial_number_option = CONF_SERIAL_NUMBER in config

    if not (has_command_option or has_type_option):
        raise cv.Invalid("You need to set either COMMAND/COMMAND_LAMBDA/COMMAND_LAMBDA_LEGACY or TYPE.")

    if has_command_option:
        if has_type_option or has_address_option or has_payload_option or has_serial_number_option:
            raise cv.Invalid("You can either set COMMAND/COMMAND_LAMBDA/COMMAND_LAMBDA_LEGACY or TYPE and ADDRESS/ADDRESS_LAMBDA, PAYLOAD/PAYLOAD_LAMBDA and SERIAL_NUMBER.")
    else:
        if not has_type_option:
            raise cv.Invalid("You need to set TYPE.")

    if CONF_COMMAND in config and (CONF_COMMAND_LAMBDA in config or CONF_COMMAND_LAMBDA_LEGACY in config):
        raise cv.Invalid("You can either set COMMAND or COMMAND_LAMBDA/COMMAND_LAMBDA_LEGACY, not both.")
    
    if CONF_ADDRESS in config and CONF_ADDRESS_LAMBDA in config:
        raise cv.Invalid("You can either set ADDRESS or ADDRESS_LAMBDA, not both.")
    
    if CONF_PAYLOAD in config and CONF_PAYLOAD_LAMBDA in config:
        raise cv.Invalid("You can either set PAYLOAD or PAYLOAD_LAMBDA, not both.")

    return config

CONFIG_SCHEMA = cv.All(
    binary_sensor.binary_sensor_schema(CommandListenerBinarySensor).extend(
        {
            cv.GenerateID(): cv.declare_id(CommandListenerBinarySensor),
            cv.GenerateID(CONF_TC_ID): cv.use_id(TCBusComponent),

            cv.Optional(CONF_COMMAND): cv.hex_uint32_t,
            cv.Optional(CONF_COMMAND_LAMBDA): cv.returning_lambda,
            cv.Optional(CONF_COMMAND_LAMBDA_LEGACY): cv.returning_lambda,
            
            cv.Optional(CONF_TYPE): cv.enum(COMMAND_TYPES, upper=False),
            cv.Optional(CONF_ADDRESS): cv.hex_uint8_t,
            cv.Optional(CONF_ADDRESS_LAMBDA): cv.returning_lambda,
            cv.Optional(CONF_PAYLOAD): cv.hex_uint32_t,
            cv.Optional(CONF_PAYLOAD_LAMBDA): cv.returning_lambda,
            cv.Optional(CONF_SERIAL_NUMBER): cv.hex_uint32_t,

            cv.Optional(CONF_ICON, default="mdi:doorbell"): cv.icon,
            cv.Optional(CONF_NAME, default="Doorbell"): cv.string,
            cv.Optional(CONF_AUTO_OFF, default="3s"): cv.positive_time_period_milliseconds
        }
    ),
    validate,
)

async def new_binary_sensor(config, *args):
    var = cg.new_Pvariable(config[CONF_ID], *args)
    await binary_sensor.register_binary_sensor(var, config)
    return var

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await binary_sensor.register_binary_sensor(var, config)

    if CONF_COMMAND_LAMBDA in config:
        command_template_ = await cg.process_lambda(
            config[CONF_COMMAND_LAMBDA], [], return_type=cg.optional.template(cg.uint32)
        )
        cg.add(var.set_command_lambda(command_template_))
    elif CONF_COMMAND_LAMBDA_LEGACY in config:
        command_template_ = await cg.process_lambda(
            config[CONF_COMMAND_LAMBDA_LEGACY], [], return_type=cg.optional.template(cg.uint32)
        )
        cg.add(var.set_command_lambda(command_template_))

    if CONF_COMMAND in config:
        cg.add(var.set_command(config[CONF_COMMAND]))

    if CONF_TYPE in config:
        cg.add(var.set_command_type(config[CONF_TYPE]))

    if CONF_ADDRESS in config:
            cg.add(var.set_address(config[CONF_ADDRESS]))

    if CONF_ADDRESS_LAMBDA in config:
        address_template_ = await cg.process_lambda(
            config[CONF_ADDRESS_LAMBDA], [], return_type=cg.optional.template(cg.uint8)
        )
        cg.add(var.set_address_lambda(address_template_))

    if CONF_PAYLOAD in config:
        cg.add(var.set_payload(config[CONF_PAYLOAD]))

    if CONF_PAYLOAD_LAMBDA in config:
        payload_template_ = await cg.process_lambda(
            config[CONF_PAYLOAD_LAMBDA], [], return_type=cg.optional.template(cg.uint32)
        )
        cg.add(var.set_payload_lambda(payload_template_))

    if CONF_SERIAL_NUMBER in config:
        cg.add(var.set_serial_number(config[CONF_SERIAL_NUMBER]))
        
    cg.add(var.set_auto_off(config[CONF_AUTO_OFF]))

    tc_bus = await cg.get_variable(config[CONF_TC_ID])
    cg.add(tc_bus.register_listener(var))