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

from .doxygen_builder import DoxygenBuilder
from .sphinx_builder import SphinxBuilder

__all__ = [
    'create_builder_by_name',
    'DoxygenBuilder',
    'SphinxBuilder',
]


def create_builder_by_name(builder_name, *, builder_dict, build_context):
    """Instantiate a new builder with the given builder_name."""
    # TODO(wjwwood): make this an extension point
    builders = {
        'doxygen': DoxygenBuilder,
        'sphinx': SphinxBuilder,
    }
    builder_class = builders.get(builder_name, None)
    if builder_class is None:
        builder_names = ', '.join(list(builders.keys()))
        raise RuntimeError(
            f"Error unknown builder '{builder_name}', supported builders: [{builder_names}]")
    return builder_class(builder_name, builder_dict, build_context)
