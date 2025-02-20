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

from pathlib import Path

template_content = """
{% extends "!layout.html" %}
{% block navigation %}
<div class="wy-menu wy-menu-vertical">
<ul>
<li class="toctree-l1">
  <a class="reference internal" href="generated/doxygen/html/">C++ API (Doxygen)</a>
</li>
</ul>
</div>
{{ super() }}
{% endblock %}
"""


def doxygen_toc_template(output_dir):
    """Create a sphinx template to show Doxygen html content in sidebar toc."""
    template_dir = Path(output_dir) / '__doxy_template'
    template_dir.mkdir(exist_ok=True)
    with open(template_dir / 'layout.html', 'w') as f:
        f.write(template_content)
