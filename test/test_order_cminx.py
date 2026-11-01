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

import logging

from rosdoc2.verbs.build.inspect_package_for_settings import order_cminx_builders


def names(builders_list):
    return [next(iter(b)) for b in builders_list]


def test_cminx_not_used():
    builders = [{'doxygen': {}}, {'sphinx': {}}]
    assert names(order_cminx_builders(builders, False)) == ['doxygen', 'sphinx']


def test_cminx_added_before_sphinx():
    builders = [{'doxygen': {}}, {'sphinx': {}}]
    assert names(order_cminx_builders(builders, True)) == ['doxygen', 'cminx', 'sphinx']


def test_cminx_added_without_sphinx():
    builders = [{'doxygen': {}}]
    assert names(order_cminx_builders(builders, True)) == ['doxygen', 'cminx']


def test_cminx_moved_before_sphinx(caplog):
    cminx = {'cminx': {'output_dir': 'custom'}}
    builders = [{'doxygen': {}}, {'sphinx': {}}, cminx]
    with caplog.at_level(logging.WARNING, logger='rosdoc2'):
        result = order_cminx_builders(builders, False)
    assert names(result) == ['doxygen', 'cminx', 'sphinx']
    assert result[1] is cminx  # user settings preserved
    assert 'after the sphinx builder' in caplog.text


def test_cminx_already_before_sphinx_no_warning(caplog):
    builders = [{'doxygen': {}}, {'cminx': {}}, {'sphinx': {}}]
    with caplog.at_level(logging.WARNING, logger='rosdoc2'):
        result = order_cminx_builders(builders, True)
    assert names(result) == ['doxygen', 'cminx', 'sphinx']
    assert caplog.text == ''
