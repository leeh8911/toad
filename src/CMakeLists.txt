# -------------------------------------------------------------------
# 1) 소스 및 헤더 파일 검색
# -------------------------------------------------------------------
# 모든 .cpp, .hpp 파일을 재귀적으로 찾아 변수에 담습니다.
file(GLOB_RECURSE ALL_CPP   "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")
file(GLOB_RECURSE ALL_HPP   "${CMAKE_CURRENT_SOURCE_DIR}/*.hpp")

# -------------------------------------------------------------------
# 2) main.cpp와 나머지 코드(라이브러리) 분리
# -------------------------------------------------------------------
# ALL_CPP 목록에서 “main.cpp” 파일만 골라 EXEC_SOURCES에 담고,
# 나머지는 LIB_SOURCES에 담도록 처리합니다.
set(EXEC_SOURCES )
set(LIB_SOURCES  )

foreach(_file IN LISTS ALL_CPP)
    # toad 디렉터리 기준으로 main.cpp 파일의 상대 경로가 toad/main.cpp 라고 가정
    if (_file MATCHES ".*[/\\\\]main\\.cpp$")
        list(APPEND EXEC_SOURCES "${_file}")
    else()
        list(APPEND LIB_SOURCES "${_file}")
    endif()
endforeach()

# (선택 사항) 헤더만 별도로 라이브러리에 포함할 필요가 없는 경우, 
# 굳이 LIB_SOURCES에 헤더를 넣지 않아도 되지만, 그냥 관리 편의를 위해 모두 두었습니다.
list(APPEND LIB_SOURCES ${ALL_HPP})

# -------------------------------------------------------------------
# 3) ltoad 라이브러리 생성
# -------------------------------------------------------------------
# LIB_SOURCES에 모인 소스(.cpp/.hpp)를 기반으로 정적 라이브러리 또는 공유 라이브러리를 만듭니다.
#
# 정적 라이브러리로 만들려면 STATIC, 공유 라이브러리로 만들려면 SHARED 옵션을 줄 수 있습니다.
add_library(${PROJECT_LIB} STATIC
    ${LIB_SOURCES}
)

# 라이브러리가 (헤더 포함을 위해) src/toad/ 디렉터리를 PUBLIC 헤더 경로로 추가
target_include_directories(${PROJECT_LIB}
    PUBLIC
        ${CMAKE_CURRENT_SOURCE_DIR}
)

# 만약 spdlog 같이 외부 패키지가 필요하다면, find_package → 링크
find_package(Spdlog REQUIRED)
target_link_libraries(${PROJECT_LIB}
    PUBLIC
        spdlog::spdlog
)

# -------------------------------------------------------------------
# 4) 실행 파일(toad) 생성
# -------------------------------------------------------------------
# main.cpp만 사용해서, 위에서 만든 ltoad 라이브러리에 링크합니다.
#
# PROJECT_NAME 은 toad/CMakeLists.txt 에서 이미 'toad' 로 선언되었으므로,
# 이 값을 이어받아 실행 파일 이름을 지었습니다.
add_executable(${PROJECT_NAME}
    ${EXEC_SOURCES}
)

# 실행 파일에 ltoad 을 연결
target_link_libraries(${PROJECT_NAME}
    PRIVATE
        ${PROJECT_LIB}
)

# 실행 파일 역시 헤더를 찾을 수 있도록 src 디렉터리를 포함
target_include_directories(${PROJECT_NAME}
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
)

# -------------------------------------------------------------------
# 5) (기존 작업) 실행 파일 이름 변경(Optional)
# -------------------------------------------------------------------
set_target_properties(${PROJECT_NAME} PROPERTIES
    OUTPUT_NAME ${PROJECT_NAME}
)

# -------------------------------------------------------------------
# 6) (선택 사항) install 규칙 추가
# -------------------------------------------------------------------
# 라이브러리와 실행 파일을 설치하려면 아래와 같이 추가할 수 있습니다.
# install(TARGETS ltoad ${PROJECT_NAME}
#     ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}   # 정적 라이브러리 설치 경로
#     RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}   # 실행 파일 설치 경로
#     LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}   # 공유 라이브러리 설치 경로
# )
