#pragma once

#include "toad/command/base_command.hpp"

namespace toad::command
{

class HelpCommand : public BaseCommand
{
 public:
    HelpCommand() = default;
    ~HelpCommand() override = default;

    // Override the execute method to provide help functionality
    void execute() override
    {
        // Implementation of help command
        // This could print available commands, options, etc.
    }
};
}  // namespace toad::command
