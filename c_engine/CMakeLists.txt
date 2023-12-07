cmake_minimum_required(VERSION 3.25)

project(chess_engine)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_FLAGS "-Wall -g")
add_definitions(-DDEBUG)

file(GLOB_RECURSE SOURCES src/*.cpp)
file(GLOB_RECURSE TESTS test/*.cpp)

add_library(board STATIC ${SOURCES})
target_include_directories(board PUBLIC include)

add_executable(engine main.cpp)
add_executable(tests ${TESTS})

target_link_libraries(engine PUBLIC board)
target_link_libraries(tests PUBLIC board)
