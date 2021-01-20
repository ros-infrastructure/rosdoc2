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

from catkin_pkg.package import has_ros_schema_reference
from catkin_pkg.package import InvalidPackage
from catkin_pkg.package import package_exists_at
from catkin_pkg.package import parse_package

from .collect_inventory_files import collect_inventory_files
from .collect_tag_files import collect_tag_files
from .inspect_package_for_settings import inspect_package_for_settings
from .setup_doc_build_prefix import setup_doc_build_prefix

DEFAULT_BUILD_OUTPUT_DIR = 'doc_build'


def get_package(path):
    """Get the ROS package for the given path."""
    if not package_exists_at(path):
        raise RuntimeError(f"Failed to find a ROS package at given path '{path}'")

    try:
        package = parse_package(path)
    except (AssertionError, InvalidPackage) as e:
        if has_ros_schema_reference(path):
            raise RuntimeError(f"Failed to parse ROS package manifest in '{path}': {e}")
        else:
            raise RuntimeError(f"Failed to parse potential ROS package manifest in '{path}': {e}")
        return None

    package.evaluate_conditions(os.environ)
    return package


def prepare_arguments(parser):
    parser.add_argument(
        '--package-path',
        '-p',
        required=True,
        help='path to the ROS package',
    )
    parser.add_argument(
        '--build-directory',
        '-b',
        required=True,
        help='build directory of the package',
    )
    parser.add_argument(
        '--install-directory',
        '-i',
        required=True,
        help='install directory of the package',
    )
    parser.add_argument(
        '--cross-reference-directory',
        '-c',
        required=True,
        help='directory containing cross reference files, like tag files and inventory files',
    )
    parser.add_argument(
        '--output-directory',
        '-o',
        default=DEFAULT_BUILD_OUTPUT_DIR,
        help='directory to output the documenation artifacts into',
    )
    parser.add_argument(
        '--doc-build-directory',
        '-d',
        default='doc_build',
        help='directory to setup build prefix'
    )
    parser.add_argument(
        '--debug',
        default=False,
        action='store_true',
        help='enable more output to debug problems'
    )
    return parser


def main(options):
    try:
        return main_impl(options)
    except Exception as e:
        if options.debug:
            raise
        else:
            sys.exit(str(e))


def main_impl(options):
    # Locate and parse the package's package.xml.
    try:
        package = get_package(options.package_path)
    except Exception as e:
        sys.exit(f'Error: {e}')

    # Check that the build directory exists.
    if not os.path.exists(options.build_directory):
        sys.exit(f"Error: given build directory '{options.build_directory}' does not exist")

    # Check that the install directory exists.
    if not os.path.exists(options.install_directory):
        sys.exit(f"Error: given install directory '{options.install_directory}' does not exist")

    # Inspect package for additional settings, using defaults if none found.
    doc_build_settings = inspect_package_for_settings(package)

    # Create the cross reference directory if it doesn't exist.
    os.makedirs(os.path.join(options.cross_reference_directory, package.name), exist_ok=True)

    # Collect Doxygen tag files in cross reference directory.
    tag_files = collect_tag_files(options.cross_reference_directory)

    # Collect Sphinx inventory files.
    inventory_files = collect_inventory_files(options.cross_reference_directory)

    # Generate the doc build prefix.
    package_doc_build_directory = os.path.join(options.doc_build_directory, package.name)
    os.makedirs(package_doc_build_directory, exist_ok=True)
    setup_doc_build_prefix(
        options.package_path,
        package_doc_build_directory,
        package,
        tag_files,
        inventory_files)

    # Create the output directory for doxygen, because it will not create it on its own.
    os.makedirs(os.path.join(package_doc_build_directory, 'generated', 'doxygen'), exist_ok=True)

    # Run the Sphinx.
    import subprocess
    subprocess.run(['sphinx-build', './', './build'], cwd=package_doc_build_directory)

    return 0
