#pragma once

#include "tc_bus.h"

#include "esphome/core/automation.h"
#include "esphome/core/component.h"

namespace esphome
{
    namespace tc_bus
    {
        template<typename... Ts> class TCBusSendAction : public Action<Ts...>
        {
            public:
                TCBusSendAction(TCBusComponent *parent) : parent_(parent) {}
                TEMPLATABLE_VALUE(uint32_t, command)
                TEMPLATABLE_VALUE(uint8_t, address)
                TEMPLATABLE_VALUE(CommandType, type)
                TEMPLATABLE_VALUE(uint32_t, serial_number)

                void play(Ts... x)
                {
                    if(this->command_.value(x...) == 0)
                    {
                        this->parent_->send_command_generate(this->type_.value(x...), this->address_.value(x...), this->serial_number_.value(x...));
                    }
                    else
                    {
                        this->parent_->send_command(this->command_.value(x...));
                    }
                }

            protected:
                TCBusComponent *parent_;
        };

        template<typename... Ts> class TCBusProgrammingModeAction : public Action<Ts...>
        {
            public:
                TCBusProgrammingModeAction(TCBusComponent *parent) : parent_(parent) {}
                TEMPLATABLE_VALUE(bool, programming_mode)

                void play(Ts... x) { this->parent_->set_programming_mode(this->programming_mode_.value(x...)); }

            protected:
                TCBusComponent *parent_;
        };

        template<typename... Ts> class TCBusReadEEPROMAction : public Action<Ts...>
        {
            public:
                TCBusReadEEPROMAction(TCBusComponent *parent) : parent_(parent) {}
                TEMPLATABLE_VALUE(uint32_t, serial_number)

                void play(Ts... x) { this->parent_->read_eeprom(this->serial_number_.value(x...)); }

            protected:
                TCBusComponent *parent_;
        };

        class ReceivedCommandTrigger : public Trigger<CommandData> {
            public:
                explicit ReceivedCommandTrigger(TCBusComponent *parent) {
                    parent->add_received_command_callback([this](const CommandData &value) { this->trigger(value); });
                }
        };
    }  // namespace tc_bus
}  // namespace esphome