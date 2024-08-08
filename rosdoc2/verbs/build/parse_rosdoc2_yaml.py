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


def parse_rosdoc2_yaml(configs, build_context):
    """
    Parse a rosdoc2.yaml configuration string, returning it as a tuple of settings and builders.

    :return: a tuple with the first item being the tool settings as a dictionary,
        and the second item being a list of Builder objects.
    """
    file_name = build_context.configuration_file_path
    if len(configs) != 2:
        raise ValueError(
            f"Error parsing file '{file_name}', "
            f"expected a YAML file with two sections, separated by '---', found {len(configs)}.")
    attic, config = configs
    if 'type' not in attic or attic['type'] != 'rosdoc2 config':
        raise ValueError(
            f"Error parsing file '{file_name}', "
            f"expected the first section of the YAML file to have a \"type: 'rosdoc2 config'\".")
    if 'version' not in attic or attic['version'] != 1:
        raise ValueError(
            f"Error parsing file '{file_name}', "
            f"expected the first section of the YAML file to have a 'version' entry, "
            'and only version 1 is supported.')
    if not isinstance(config, dict):
        raise ValueError(
            f"Error parsing file '{file_name}', in the second section, "
            f'expected something like dict{{settings: <tool settings>, builders: <builders>}}, '
            f"got a '{type(config)}' instead")

    if 'settings' not in config:
        raise ValueError(
            f"Error parsing file '{file_name}', in the second section, "
            f"expected a 'settings' key")
    settings_dict = config['settings']
    if not isinstance(settings_dict, dict):
        raise ValueError(
            f"Error parsing file '{file_name}', in the second section, value 'settings', "
            f'expected a dict{{output_dir: build_settings, ...}}, '
            f"got a '{type(settings_dict)}' instead")

    if 'builders' not in config:
        raise ValueError(
            f"Error parsing file '{file_name}', in the second section, "
            f"expected a 'builders' key")
    builders_list = config['builders']
    if not isinstance(builders_list, list):
        raise ValueError(
            f"Error parsing file '{file_name}', in the second section, value 'builders', "
            'expected a list of builders, '
            f"got a '{type(builders_list)}' instead")

    for builder in builders_list:
        if len(builder) != 1:
            raise ValueError(
                f"Error parsing file '{file_name}', in the second section, each builder "
                'must have exactly one key (which is the type of builder to use)')

    return (settings_dict, builders_list)
