# Copyright 2022 Open Source Robotics Foundation, Inc.
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


"""Generate rst files for messages, services, and actions."""

import fnmatch
import os

iface_fm_rst = """\
{iface_name}
{name_underline}
This is a ROS {type_name} definition.

**Source**

.. literalinclude:: {relative_path}

"""

toc_fm_rst = """\
{title}
{title_underline}

.. toctree::
   :maxdepth: 1
   :glob:

   {type_ext}/*

"""


def _find_files_with_extension(path, ext):
    # Partly adapted from https://github.com/ros-infrastructure/rosdoc_lite
    matches = []
    for root, _, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, f'*.{ext}'):
            matches.append((os.path.splitext(filename)[0], os.path.join(root, filename)))
    return matches


def generate_interface_docs(path: str, package: str, output_dir: str):
    """
    Generate rst files from messages and services.

    :param str path: Directory path to start search for files
    :param str package: Name of containing package
    :param str output_dir: Directory path to write output
    :return: {'msg':msg_count, 'srv':srv_count} count of files written
    :rtype: dict(str, int)
    """
    counts = {}
    for type_info in (('msg', 'message'), ('srv', 'service'), ('action', 'action')):
        count = 0
        (type_ext, type_name) = type_info
        interfaces = _find_files_with_extension(path, type_ext)
        output_dir_ex = os.path.join(output_dir, type_ext)
        title = type_name.capitalize() + ' Definitions'
        for interface in interfaces:
            (iface_name, iface_path) = interface
            relative_path = os.path.relpath(iface_path, start=output_dir_ex)
            template_vars = {
                'iface_name': iface_name,
                'name_underline': '=' * len(iface_name),
                'type_name': type_name,
                'package': package,
                'type_ext': type_ext,
                'relative_path': relative_path,
                'title': title,
                'title_underline': '=' * len(title)
            }
            iface_rst = iface_fm_rst.format_map(template_vars)

            if not os.path.exists(output_dir_ex):
                os.makedirs(output_dir_ex)
            output_path = os.path.join(output_dir_ex, f'{iface_name}.rst')
            with open(output_path, 'w') as f:
                f.write(iface_rst)
            count += 1
        if count > 0:
            # generate a toc entry rst file for this type
            toc_rst = toc_fm_rst.format_map(template_vars)
            toc_name = type_name + '_definitions.rst'
            toc_path = os.path.join(output_dir, toc_name)
            with open(toc_path, 'w') as f:
                f.write(toc_rst)
        counts[type_ext] = count
    return counts
