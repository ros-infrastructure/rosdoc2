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

import re


def slugify(
    string,
    *,
    lowercase=True,
    whitespace=False,
    whitespace_replacement='-',
):
    """
    Convert the given string into a "slug" which can be safely used in a directory name.

    This function is naive, and doesn't handle unicode or anything special.
    If we need that in the future, consider something like python-slugify.
    """
    slug = string
    if lowercase:
        slug = slug.lower()
    slug = re.sub(r'[^\w\s]', '', slug)
    if not whitespace:
        slug = re.sub(r'\s+', whitespace_replacement, slug)
    return slug
