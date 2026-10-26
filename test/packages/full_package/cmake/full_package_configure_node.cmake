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
# Configure an executable target as a full_package node.
#
# :param target: the name of the executable target
# :type target: string
# :param RATE: the publishing rate in Hz, default: 10
# :type RATE: string
#
# .. note:: The target must already exist.
#]]
function(full_package_configure_node target)
  cmake_parse_arguments(ARG "" "RATE" "" ${ARGN})
  if(NOT ARG_RATE)
    set(ARG_RATE "${FULL_PACKAGE_DEFAULT_RATE}")
  endif()
  target_compile_definitions(${target} PRIVATE "FULL_PACKAGE_RATE=${ARG_RATE}")
endfunction()

#[[[
# The default publishing rate used by :func:`full_package_configure_node`.
#]]
set(FULL_PACKAGE_DEFAULT_RATE "10")
