#pragma once

#include "esphome/core/hal.h"

namespace esphome
{
    namespace tc_bus
    {
        enum CommandType {
            COMMAND_TYPE_UNKNOWN,
            COMMAND_TYPE_DOOR_CALL,
            COMMAND_TYPE_FLOOR_CALL,
            COMMAND_TYPE_INTERNAL_CALL,
            COMMAND_TYPE_CONTROL_FUNCTION,
            COMMAND_TYPE_START_TALKING_DOOR_STATION,
            COMMAND_TYPE_START_TALKING_IA,
            COMMAND_TYPE_STOP_TALKING_DOOR_STATION,
            COMMAND_TYPE_STOP_TALKING_IA,
            COMMAND_TYPE_OPEN_DOOR,
            COMMAND_TYPE_LIGHT,
            COMMAND_TYPE_DOOR_OPENED,
            COMMAND_TYPE_DOOR_CLOSED,
            COMMAND_TYPE_END_OF_RINGTONE,
            COMMAND_TYPE_END_OF_DOOR_READINESS,
            COMMAND_TYPE_INITIALIZE_DOOR_STATION,
            COMMAND_TYPE_RESET,
            COMMAND_TYPE_SELECT_DEVICE_GROUP,
            COMMAND_TYPE_SELECT_DEVICE_GROUP_RESET,
            COMMAND_TYPE_SEARCH_DEVICES,
            COMMAND_TYPE_FOUND_DEVICE,
            COMMAND_TYPE_FOUND_DEVICE_SUBSYSTEM,
            COMMAND_TYPE_PROGRAMMING_MODE,
            COMMAND_TYPE_READ_EEPROM_BLOCK,
            COMMAND_TYPE_SELECT_EEPROM_PAGE
        };

        struct CommandData {
            uint32_t command;
            std::string command_hex;
            CommandType type;
            uint8_t address;
            uint32_t serial_number;
            uint8_t length;
        };

        uint32_t buildCommand(CommandType type, uint8_t address, uint32_t serial_number);
        CommandData parseCommand(uint32_t command);

        const char* command_type_to_string(CommandType type);
    }  // namespace tc_bus
}  // namespace esphome