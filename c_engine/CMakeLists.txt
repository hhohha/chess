cmake_minimum_required(VERSION 3.25)

project(chess_engine)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


# set(CMAKE_CXX_FLAGS "-Wall -Wextra -g")
# add_definitions(-DDEBUG)
set(CMAKE_CXX_FLAGS "-O3")

file(GLOB_RECURSE SOURCES src/*.cpp)
file(GLOB_RECURSE TESTS test/*.cpp)

add_library(board SHARED ${SOURCES})
add_executable(tests ${TESTS})
add_executable(engine main.cpp)

target_include_directories(engine PUBLIC include)
target_include_directories(tests PUBLIC include)
target_include_directories(board PUBLIC include)

target_link_libraries(tests PUBLIC board)
target_link_libraries(engine PUBLIC board)