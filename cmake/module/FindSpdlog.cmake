# FindSpdlog.cmake
message(STATUS "[FindSpdlog] Loaded custom FindSpdlog.cmake")

# 시도: 시스템에서 spdlog 헤더 찾기
find_path(SPDLOG_INCLUDE_DIR spdlog/spdlog.h)

if (SPDLOG_INCLUDE_DIR)
    add_library(spdlog::spdlog INTERFACE IMPORTED)
    set_target_properties(spdlog::spdlog PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${SPDLOG_INCLUDE_DIR}"
    )
    set(spdlog_FOUND TRUE)
else()
    # 시스템에서 못 찾은 경우 → FetchContent로 다운로드 시도
    message(STATUS "spdlog not found in system — fetching via FetchContent")

    include(FetchContent)
    FetchContent_Declare(
        spdlog
        GIT_REPOSITORY https://github.com/gabime/spdlog.git
        GIT_TAG v1.13.0
    )
    FetchContent_MakeAvailable(spdlog)

    # FetchContent로 가져온 타겟 사용 설정
    set(spdlog_FOUND TRUE)
endif()
