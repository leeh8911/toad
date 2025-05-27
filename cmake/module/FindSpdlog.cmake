# FindSpdlog.cmake

find_path(SPDLOG_INCLUDE_DIR spdlog/spdlog.h)
if (SPDLOG_INCLUDE_DIR)
    add_library(spdlog::spdlog INTERFACE IMPORTED)
    set_target_properties(spdlog::spdlog PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${SPDLOG_INCLUDE_DIR}"
    )
    set(spdlog_FOUND TRUE)
else()
    set(spdlog_FOUND FALSE)
endif()
