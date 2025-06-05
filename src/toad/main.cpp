#include <iostream>
#include <string>

#include "toad/command/command_handler.hpp"

#include "toad/logger.hpp"

void SetCommands()
{
    auto handler = ::toad::command::CommandHandler::getInstance();

    handler.setCommand("help");
}
int main(int argc, char* argv[])
{
    TOAD_INFO("Toad started with {} arguments", argc);

    auto tokenizer = ::toad::command::Tokenizer();

    // ::toad::command::Parser parser{};
    // if (argc < 2)
    // {
    //     TOAD_INFO("Call HelpOption");
    //     parser.option("help");
    //     return 0;
    // }

    // int index = 1;
    // while (index <= argc)
    // {
    //     std::string arg = argv[index];
    //     if (arg.starts_with('--'))
    //     {
    //         TOAD_INFO("Option called: {}", arg);
    //         parser.option(arg.substr(2), argv[index + 1]);
    //         index += 2;
    //     }
    //     else
    //     {
    //         TOAD_INFO("Command called: {}", arg);
    //         parser.command(arg);
    //         index += 1;
    //     }
    // }
    return 0;
}
