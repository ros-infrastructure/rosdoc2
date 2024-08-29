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

import os
import sys
import webbrowser

from ..build.impl import DEFAULT_OUTPUT_DIR


def prepare_arguments(parser):
    """Add command-line arguments to the argparse object."""
    parser.add_argument(
        'package_output_directory',
        nargs='?',
        default=DEFAULT_OUTPUT_DIR,
        help=f'(optional) path to the built documentation (default "{DEFAULT_OUTPUT_DIR}") '
             'OR package name',
    )
    return parser


def main(options):
    """Open a web browser to display the built documentation."""
    # Locate the entry point for the built documentation.
    path_to_open = None
    if os.path.isdir(options.package_output_directory):
        path_to_open = options.package_output_directory
        # Maybe this is a package directory?
        if os.path.isfile(os.path.join(path_to_open, 'index.html')):
            # open it directly
            path_to_open = os.path.join(path_to_open, 'index.html')
    elif os.path.isfile(options.package_output_directory):
        path_to_open = options.package_output_directory
    else:
        # Last chance: the default output_dir plus a package name
        candidate = os.path.join(
            DEFAULT_OUTPUT_DIR, options.package_output_directory, 'index.html')
        if os.path.isfile(candidate):
            path_to_open = candidate

    if path_to_open:
        webbrowser.open(f'file://{os.path.abspath(path_to_open)}')
    else:
        sys.exit('did not find package documentation at given package_output_directory '
                 f'"{options.package_output_directory}"')
