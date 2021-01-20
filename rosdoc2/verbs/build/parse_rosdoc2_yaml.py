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

import yaml

from .builders import create_builder_by_name
from .build_context import BuildContext


def parse_builder_entry(output_directory, builder_dict, build_context):
    """
    Parse a single builder dictionary entry.
    """
    if 'builder' not in builder_dict:
        keys = ', '.join(list(builder_dict.keys()))
        raise ValueError(
            f"Error parsing file '{build_context.configuration_file_path}', "
            f"expected to find a 'builder' key but found only '[{keys}]'")
    return create_builder_by_name(
        builder_dict['builder'],
        builder_dict=builder_dict,
        output_dir=output_directory,
        build_context=build_context)


def parse_rosdoc2_yaml(yaml_string, package, file_name):
    """
    Parse a rosdoc2.yaml configuration string, returning it as a list of dictionaries.

    :return: a list of Builder objects
    """
    config = yaml.load(yaml_string, Loader=yaml.SafeLoader)
    if not isinstance(config, dict):
        raise ValueError(
            f"Error parsing file '{file_name}', "
            f"expected a dict{{output_dir: build_settings, ...}}, got a '{type(config)}' instead")
    builders = []
    build_context = BuildContext(
        configuration_file_path=file_name,
        package_object=package,
    )
    for output_directory, entry in config.items():
        builders.append(parse_builder_entry(output_directory, entry, build_context))
    return builders
