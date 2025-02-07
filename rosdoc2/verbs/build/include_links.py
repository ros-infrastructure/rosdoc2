# Copyright 2024 R. Kent James <kent@caspia.com>
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

from jinja2 import Template

links_template = """
Links
=====

.. toctree::

   Rosindex <https://index.ros.org/p/{{package.name}}>
{%- for link in package.urls %}
   {{ link.type.capitalize() }} <{{ link.url }}>
{%- endfor %}
"""


def include_links(package, output_dir):
    """Generate an rst file containing links."""
    links_rst = Template(links_template).render({'package': package})
    with open(os.path.join(output_dir, '__links.rst'), 'w') as f:
        f.write(links_rst)
