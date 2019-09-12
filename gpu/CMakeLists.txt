cmake_minimum_required(VERSION 3.7)

find_package(OpenCL REQUIRED)

add_executable(main main.cpp)

set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR})
target_link_libraries(main OpenCL::OpenCL)