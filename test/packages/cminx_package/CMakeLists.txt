cmake_minimum_required(VERSION 3.8)
project(cminx_package NONE)

find_package(ament_cmake_core REQUIRED)

install(
  DIRECTORY cmake
  DESTINATION share/${PROJECT_NAME}
)

ament_package(
  CONFIG_EXTRAS "cminx_package-extras.cmake"
)
