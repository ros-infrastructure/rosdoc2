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

import json
import logging
import os

logger = logging.getLogger('rosdoc2')


def collect_inventory_files(cross_reference_directory, depends):
    """
    Collect all inventory files of a given cross reference directory.

    :return: dictionary of inventory files, where the package name is the key
    """
    inventory_files = {}
    for root, directories, filenames in os.walk(cross_reference_directory):
        for filename in filenames:
            if filename == 'objects.inv':
                # The parent folder should be a package name.
                package_name = os.path.basename(root)
                if package_name in inventory_files:
                    raise RuntimeError(
                        f"unexpectedly got duplicate tag file for package '{package_name}'"
                    )
                # only include if in depends list
                if package_name not in depends:
                    continue
                inventory_file_path = os.path.join(root, filename)
                location_json_path = inventory_file_path + '.location.json'
                if not os.path.exists(location_json_path):
                    logger.warn(
                        f"Ignoring tag file '{inventory_file_path}' because it lacks "
                        f"a '.location.json' file.")
                    continue
                location_data = None
                with open(location_json_path, 'r+') as f:
                    location_data = json.loads(f.read())
                inventory_files[package_name] = {
                    'inventory_file': inventory_file_path,
                    'location_data': location_data,
                }
    return inventory_files
