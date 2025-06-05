#pragma once

#include <memory>

#include "toad/registry/registry.hpp"

namespace toad::command
{
class BaseCommand
{
 public:
    BaseCommand() = default;
    virtual ~BaseCommand() = default;

    // Pure virtual function to be implemented by derived classes
    virtual void execute() = 0;

    // Optional: You can add a method to get the command name or description
    virtual const char* name() const = 0;
    virtual const char* description() const = 0;

    // Optional: You can add a method to check if the command is valid
    virtual bool is_valid() const
    {
        return true;
    }

 private:
};

using CommandRegistry = ::toad::registry::Registry<BaseCommand>;

using BaseCommandPtr = std::unique_ptr<BaseCommand>;

}  // namespace toad::command
