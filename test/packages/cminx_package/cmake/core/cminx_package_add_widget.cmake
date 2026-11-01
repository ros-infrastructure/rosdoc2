# Copyright 2026 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#[[[
# Add a widget target to the current project.
#
# The widget is a custom target which prints its name when built.
#
# :param target: the name of the widget target
# :type target: string
# :param COLOR: the color of the widget, default: blue
# :type COLOR: string
# :param SHINY: if set, the widget is shiny
# :type SHINY: option
#
# .. note:: Widgets are purely decorative and are not installed.
#]]
function(cminx_package_add_widget target)
  cmake_parse_arguments(ARG "SHINY" "COLOR" "" ${ARGN})
  if(NOT ARG_COLOR)
    set(ARG_COLOR "blue")
  endif()
  add_custom_target(${target} ALL
    COMMAND ${CMAKE_COMMAND} -E echo "Widget ${target} is ${ARG_COLOR}")
endfunction()

#[[[
# The default color used by :func:`cminx_package_add_widget`.
#]]
set(CMINX_PACKAGE_DEFAULT_COLOR "blue")
