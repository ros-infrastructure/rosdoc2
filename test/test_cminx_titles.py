# Copyright 2026 Open Source Robotics Foundation, Inc.
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

from rosdoc2.verbs.build.builders.cminx_builder import shorten_cminx_titles


def cminx_rst(title):
    """Return rst in the form cminx generates, with a module of the same name as the title."""
    line = '#' * len(title)
    return f'\n{line}\n{title}\n{line}\n\n.. module:: {title}\n\n'


def write_rst(path, title):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(cminx_rst(title))


def test_shorten_cminx_titles(tmp_path):
    write_rst(tmp_path / 'index.rst', 'my_pkg')
    write_rst(tmp_path / 'top_level.rst', 'my_pkg.top_level')
    write_rst(tmp_path / 'core' / 'index.rst', 'my_pkg.core')
    write_rst(tmp_path / 'core' / 'my_pkg_add_widget.rst', 'my_pkg.core/my_pkg_add_widget')
    write_rst(tmp_path / 'core' / 'custom.rst', 'MyCustomModule')

    shorten_cminx_titles(str(tmp_path), 'my_pkg')

    assert (tmp_path / 'index.rst').read_text() == cminx_rst('my_pkg')
    assert (tmp_path / 'top_level.rst').read_text() == \
        '\n#########\ntop_level\n#########\n\n.. module:: my_pkg.top_level\n\n'
    assert (tmp_path / 'core' / 'index.rst').read_text() == \
        '\n####\ncore\n####\n\n.. module:: my_pkg.core\n\n'
    assert (tmp_path / 'core' / 'my_pkg_add_widget.rst').read_text() == \
        '\n#################\nmy_pkg_add_widget\n#################\n\n' \
        '.. module:: my_pkg.core/my_pkg_add_widget\n\n'
    assert (tmp_path / 'core' / 'custom.rst').read_text() == cminx_rst('MyCustomModule')
