#include <iostream>

#include "toad/logger.hpp"

int main(int argc, char* argv[])
{
    TOAD_INFO("Toad started with {} arguments", argc);
    return 0;
}
