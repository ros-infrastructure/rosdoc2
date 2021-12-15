# Copyright 2020 Open Source Robotics Foundation, Inc.
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


class BuildContext:
    """
    Class which encapsulates the context of the build.

    Used to calculate default settings for builders based on things like the
    package directory, when necessary.
    """

    def __init__(self, *, configuration_file_path, package_object, tool_options):
        """Construct a new BuildContext."""
        self.configuration_file_path = configuration_file_path
        self.package = package_object
        self.tool_options = tool_options
