cmake_minimum_required(VERSION 3.10)

project(chess_engine)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_FLAGS "-Wall")
set(CMAKE_BINARY_DIR, "build/")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# Add all the source files to the project
file(GLOB_RECURSE SOURCES src/*.cpp)

# Add the executable target
add_executable(chess_engine ${SOURCES})

# Add include directories
target_include_directories(chess_engine PUBLIC include)

