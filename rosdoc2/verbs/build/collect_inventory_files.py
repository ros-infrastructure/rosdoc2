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


def collect_inventory_files(cross_reference_directory):
    """
    Collect all inventory files if a given cross reference directory.

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
                inventory_files[package_name] = os.path.join(root, filename)
    return inventory_files
