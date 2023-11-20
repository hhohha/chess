cmake_minimum_required(VERSION 3.10)

project(chess_engine)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_FLAGS "-Wall -g")
set(CMAKE_BINARY_DIR, "build/")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# Add all the source files to the project
file(GLOB_RECURSE SOURCES src/*.cpp)
file(GLOB_RECURSE TESTS test/*.cpp)

# Add the executable target
add_executable(engine ${SOURCES} main.cpp)
add_executable(tests ${TESTS} ${SOURCES})

# Add include directories
target_include_directories(engine PUBLIC include)
target_include_directories(tests PUBLIC include)

