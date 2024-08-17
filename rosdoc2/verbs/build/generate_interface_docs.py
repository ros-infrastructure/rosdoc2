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

import os
import shutil

iface_fm_rst = """\
{iface_base}
{name_underline}
This is a ROS {type_name} definition.

**Source**

.. literalinclude:: {iface_name}

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
    """
    Search a package path, in subdirectory <ext>, for files with that <ext>.
    """
    # Partly adapted from https://github.com/ros-infrastructure/rosdoc_lite
    matches = []
    # We assume that the directory name is the same as the extension
    iface_dir = os.path.join(path, ext)
    if not os.path.isdir(iface_dir):
        return matches
    for filename in os.listdir(iface_dir):
        filepath = os.path.join(iface_dir, filename)
        (filebase, fileext) = os.path.splitext(filename)
        if os.path.isfile(filepath) and (ext == fileext[1:]):
            matches.append((filename, filepath, filebase))
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
            (iface_name, iface_path, iface_base) = interface
            template_vars = {
                'iface_base': iface_base,
                'iface_name': iface_name,
                'name_underline': '=' * len(iface_base),
                'type_name': type_name,
                'type_ext': type_ext,
                'title': title,
                'title_underline': '=' * len(title)
            }
            iface_rst = iface_fm_rst.format_map(template_vars)

            if not os.path.exists(output_dir_ex):
                os.makedirs(output_dir_ex)
            output_path = os.path.join(output_dir_ex, f'{iface_base}.rst')
            with open(output_path, 'w') as f:
                f.write(iface_rst)
            shutil.copyfile(iface_path, os.path.join(output_dir_ex, iface_name))
            count += 1
        if count > 0:
            # generate a toc entry rst file for this type
            toc_rst = toc_fm_rst.format_map(template_vars)
            toc_name = '__' + type_name + '_definitions.rst'
            toc_path = os.path.join(output_dir, toc_name)
            with open(toc_path, 'w') as f:
                f.write(toc_rst)
        counts[type_ext] = count
    return counts
