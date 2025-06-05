#pragma once

#include <memory>
#include <vector>

#include "toad/command/base_command.hpp"
#include "toad/mixin/singleton.hpp"

namespace toad::command
{
class CommandHandler : public ::toad::mixin::Singleton<CommandHandler>
{
 public:
    void setCommand(const std::string& command_name);

 private:
    std::vector<std::unique_ptr<BaseCommand>> commands{};
};
}  // namespace toad::command
