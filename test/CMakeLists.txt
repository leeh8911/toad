# -------------------------------------------------------------------
# 1) GoogleTest FetchContent로 가져오기
# -------------------------------------------------------------------
include(FetchContent)

set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_Declare(
  googletest
  URL  https://github.com/google/googletest/archive/refs/tags/release-1.12.1.zip
  DOWNLOAD_EXTRACT_TIMESTAMP TRUE
)
FetchContent_MakeAvailable(googletest)

# -------------------------------------------------------------------
# 2) 테스트용 실행 파일 정의
# -------------------------------------------------------------------

file(GLOB_RECURSE TEST_SOURCES "${CMAKE_CURRENT_SOURCE_DIR}/*.cpp")

add_executable(toad_test
  ${TEST_SOURCES}
)

# -------------------------------------------------------------------
# 3) 헤더 검색 경로 설정
# -------------------------------------------------------------------
# 프로젝트의 소스 코드(라이브러리)가 src/ 디렉터리 아래에 있다고 가정합니다.
# 예를 들어, src/toad/registry/registry.hpp 같은 헤더를 포함해야 할 때
# "${CMAKE_SOURCE_DIR}/src"를 추가해 주면 됩니다.
#
# CMAKE_SOURCE_DIR는 최상위 CMakeLists.txt가 있는 디렉터리(프로젝트 루트)를 가리킵니다.
target_include_directories(toad_test PRIVATE
  ${CMAKE_SOURCE_DIR}/src
)

# -------------------------------------------------------------------
# 4) 소스 라이브러리(또는 코드)와 GoogleTest 링크
# -------------------------------------------------------------------
# 4-1) 만약 src/CMakeLists.txt에서 "toad"라는 이름의 라이브러리( add_library(toad ...) )를 만들었다면,
#      아래처럼 toad 라이브러리와 gtest_main을 링크합니다.
#
#    예시: src/CMakeLists.txt 내부에
#      add_library(toad
#        toad/registry/registry.hpp
#        toad/registry/registry_macro.hpp
#        toad/logger.hpp
#        toad/...)
#      target_include_directories(toad PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/toad)
#
#    이럴 경우 테스트 타겟에서는 아래처럼 링크만 해 주면 됩니다.
target_link_libraries(toad_test
  PRIVATE
    ${PROJECT_LIB}         # src/에서 정의한 toad 라이브러리 타겟
    gtest_main   # GoogleTest 메인
)

# 5-2) 만약 src 쪽에 아직 라이브러리 타겟이 없다면,
#      아래처럼 소스 파일(.cpp)을 직접 나열해서 컴파일하거나,
#      (비권장) src/CMakeLists.txt를 수정하여 반드시 add_library(toad ...) 형태로 라이브러리를 만들어 두는 것을 권장합니다.

# -------------------------------------------------------------------
# 6) 테스트 케이스 자동 등록 (gtest_discover_tests)
# -------------------------------------------------------------------
# toad_test 안에 정의된 TEST(...) 매크로를 자동으로 CTest에 등록합니다.
include(GoogleTest)
gtest_discover_tests(toad_test
  # (옵션) 테스트 실행 시 타임아웃을 5초로 설정
  DISCOVERY_TIMEOUT 5.0
)

# 끝.
