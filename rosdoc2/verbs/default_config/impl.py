# Copyright 2024 Jonas Otto
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

import os

from ..build.create_format_map_from_package import create_format_map_from_package
from ..build.impl import get_package
from ..build.inspect_package_for_settings import DEFAULT_ROSDOC_CONFIG_FILE


def prepare_arguments(parser):
    """Add command-line arguments to the argparse object."""
    parser.add_argument(
        '--package-path',
        '-p',
        required=True,
        help='path to the ROS package',
    )
    return parser


def main(options):
    """Execute command to create default config file."""
    package = get_package(options.package_path)
    path = os.path.join(os.path.dirname(package.filename), 'rosdoc2.yaml')
    if os.path.exists(path):
        print(f'Config file already exists at {path}, '
              'remove it and run again to replace it with the default.')
        return

    package_map = create_format_map_from_package(package)
    rosdoc_config_file = DEFAULT_ROSDOC_CONFIG_FILE.format_map(package_map)

    with open(path, 'w') as config_file:
        config_file.write(rosdoc_config_file)
    print('Created rosdoc2.yaml, remember to add \"<rosdoc2>rosdoc2.yaml</rosdoc2>\" '
          f'to the \"export\" section in {package.filename}')
