cmake_minimum_required(VERSION 3.25)

project(chess_engine)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


# set(CMAKE_CXX_FLAGS "-Wall -Wextra -g")
# add_definitions(-DDEBUG)
set(CMAKE_CXX_FLAGS "-O3")

file(GLOB_RECURSE SOURCES src/*.cpp)
file(GLOB_RECURSE TESTS test/*.cpp)

add_library(dboard SHARED python_wrapper.cpp ${SOURCES})
add_library(board STATIC ${SOURCES})

target_include_directories(board PUBLIC include)
target_include_directories(dboard PUBLIC include)
target_include_directories(dboard PUBLIC "$pybind11_INCLUDE_DIR")
target_include_directories(dboard PUBLIC "/usr/local/lib/python3.10/dist-packages/pybind11/include")
target_include_directories(dboard PUBLIC "/usr/include/python3.10")

add_executable(tests ${TESTS})

target_link_libraries(tests PUBLIC board)