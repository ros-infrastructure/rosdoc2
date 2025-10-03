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


def collect_tag_files(cross_reference_directory, depends):
    """Collect all tag files if a given cross reference directory."""
    tag_files = {}
    for root, directories, filenames in os.walk(cross_reference_directory):
        for filename in filenames:
            filename_base, filename_ext = os.path.splitext(filename)
            if filename_ext == '.tag':
                if filename_base not in depends:
                    # Only include tag files for packages we depend on.
                    continue
                # The filename_base should be a package name.
                if filename_base in tag_files:
                    raise RuntimeError(
                        f"unexpectedly got duplicate tag file for package '{filename_base}'"
                    )
                tag_file_path = os.path.join(root, filename)
                location_json_path = tag_file_path + '.location.json'
                if not os.path.exists(location_json_path):
                    logger.warn(
                        f"Ignoring tag file '{tag_file_path}' because it lacks "
                        f"a '.location.json' file.")
                    continue
                location_data = None
                with open(location_json_path, 'r+') as f:
                    location_data = json.loads(f.read())
                tag_files[filename_base] = {
                    'tag_file': tag_file_path,
                    'location_data': location_data,
                }
    return tag_files
