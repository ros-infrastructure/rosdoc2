# Copyright 2025 R. Kent James <kent@caspia.com>
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


"""Generate rst file ros package dependencies."""

import os

from jinja2 import Template

depends_fm_rst = """\
ROS Package Dependencies
========================

.. toctree::
    :maxdepth: 2
    {% for package_depend in package_depends %}
    {{ package_depend }} <https://docs.ros.org/en/{{ rosdistro }}/p/{{ package_depend }}/>
    {% endfor %}
"""


def generate_ros_package_dependencies(output_dir: str, package_depends: list[str], rosdistro: str):
    """
    Generate rst file for ros package dependencies.

    :param str output_dir: Directory path to write output
    :param list[str] package_depends: List of package dependencies
    :param str rosdistro: Name of ROS distribution
    """
    depends_rst = Template(depends_fm_rst).render({
        'package_depends': package_depends,
        'rosdistro': rosdistro,
    })
    toc_path = os.path.join(output_dir, '__ros_package_dependencies.rst')
    with open(toc_path, 'w') as f:
        f.write(depends_rst)
