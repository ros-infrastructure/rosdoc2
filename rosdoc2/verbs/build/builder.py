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


class Builder(object):
    """
    Base class for all builders, which just takes care of some boilerplate logic.
    """
    def __init__(self, builder_entry_dictionary, output_dir, build_context):
        if 'builder' not in builder_entry_dictionary:
            raise RuntimeError("Error entry without 'builder' field found")
        self.builder_type = builder_entry_dictionary['builder']
        if 'name' not in builder_entry_dictionary:
            raise RuntimeError("Error entry without 'name' field found")
        self.name = builder_entry_dictionary['name']
        self.builder_entry_dictionary = builder_entry_dictionary
        self.output_dir = output_dir
        self.build_context = build_context

    def build(self):
        """
        Method called on builders to have them actually do the build.
        """
        raise NotImplementedError("Should be implemented by subclasses of Builder.")
