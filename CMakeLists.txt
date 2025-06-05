cmake_minimum_required(VERSION 3.14)

project(toad)
set(PROJECT_VERSION 0.0.0)

set(PROJECT_LIB "ltoad")
set(PROJECT_TEST "toad_test")

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

set(BUILD_TESTING ON CACHE BOOL "Build testing targets")

# CMake 모듈 경로 추가
set(CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/module" ${CMAKE_MODULE_PATH})

# 설치 경로 기본값 설정
include(GNUInstallDirs)

add_subdirectory(src)

if (BUILD_TESTING)
    message(STATUS "Building tests...")
    enable_testing()
    add_subdirectory(test)
endif (BUILD_TESTING)


install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)