#pragma once

#include <memory>

#include <spdlog/sinks/basic_file_sink.h>
#include <spdlog/sinks/stdout_color_sinks.h>
#include <spdlog/spdlog.h>

#include "toad/mixin/singleton.hpp"

namespace toad
{
class Logger : public ::toad::mixin::Singleton<Logger>
{
 public:
    Logger()
    {
        if (!spdlog::get("toad"))
            logger = spdlog::stdout_color_mt("toad");
        else
            logger = spdlog::get("toad");

        logger->set_level(spdlog::level::info);
        logger->set_pattern("[%Y-%m-%d %H:%M:%S.%e] [%n] [%^%l%$] %v");
    }

    ~Logger() = default;

    void set_level(spdlog::level::level_enum level)
    {
        if (logger)
        {
            logger->set_level(level);
        }
    }
    template <typename... Args>
    void log(spdlog::level::level_enum level, fmt::format_string<Args...> format, Args&&... args)
    {
        if (logger)
        {
            logger->log(level, format, std::forward<Args>(args)...);
        }
    }

 private:
    std::shared_ptr<spdlog::logger> logger{nullptr};
};
}  // namespace toad

#define TOAD_TRACE(format, ...) \
    toad::Logger::getInstance().log(spdlog::level::trace, format, __VA_ARGS__)
#define TOAD_DEBUG(format, ...) \
    toad::Logger::getInstance().log(spdlog::level::debug, format, __VA_ARGS__)
#define TOAD_INFO(format, ...) \
    toad::Logger::getInstance().log(spdlog::level::info, format, __VA_ARGS__)
#define TOAD_WARN(format, ...) \
    toad::Logger::getInstance().log(spdlog::level::warn, format, __VA_ARGS__)
#define TOAD_ERROR(format, ...) \
    toad::Logger::getInstance().log(spdlog::level::err, format, __VA_ARGS__)
#define TOAD_CRITICAL(format, ...) \
    toad::Logger::getInstance().log(spdlog::level::critical, format, __VA_ARGS__)
