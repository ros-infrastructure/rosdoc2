# Copyright 2024 Open Source Robotics Foundation, Inc.
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
import os
from pathlib import Path
import shutil

from rosdoc2.slugify import slugify

logger = logging.getLogger('rosdoc2')

documentation_rst_template = """\
Documentation
=============

.. toctree::
   :maxdepth: 1
   :glob:

   user_docs/*
"""

subdirectory_rst_template = """\
DOCUMENTATION DIRECTORY /{name}/
========================={name_underline}=

.. toctree::
   :maxdepth: 2
   :glob:

   user_docs/{name}/*
"""


def include_user_docs(package_dir: str,
                      output_dir: str,
                      ):
    """Generate rst files for user documents."""
    doclist = {}

    logger.info(f'include_user_docs: package_dir {package_dir} output_dir {output_dir}')
    # Search the ./doc directory
    doc_dir = os.path.join(package_dir, 'doc')
    # locate and copy all documentation in package
    for root, directories, files in os.walk(doc_dir):
        for file in files:
            print(f'root {root} file {file}')

        relpath = os.path.relpath(root, doc_dir) or '.'
        # Use forward slash path separators in sphinx documents
        # relpath = relpath.replace('\\', '/')
        # ensure a valid documentation file exists
        for file in files:
            (filename, ext) = os.path.splitext(file)
            if ext in ['.rst', '.md', '.markdown']:
                if relpath not in doclist:
                    doclist[relpath] = []
                doclist[relpath].append(filename)
                directory = os.path.join(output_dir, 'user_docs')
                if relpath != '.':
                    directory = os.path.join(directory, relpath)
                Path(directory).mkdir(parents=True, exist_ok=True)
                shutil.copy(os.path.join(root, file), directory)

    toc_content = documentation_rst_template
    # generate a glob rst entry for each directory with documents
    for relpath in doclist:
        # directories that will be explicitly listed in index.rst
        if relpath == '.':
            continue
        docname = 'user_docs_' + slugify(relpath)  # This is the name that sphinx uses
        content = subdirectory_rst_template.format_map(
            {'name': relpath, 'name_underline': '=' * len(relpath)})
        sub_path = os.path.join(output_dir, docname + '.rst')
        with open(sub_path, 'w+') as f:
            f.write(content)
        toc_content += f'   {relpath} <{docname}>\n'

    if doclist:
        sub_path = os.path.join(output_dir, 'user_docs.rst')
        with open(sub_path, 'w+') as f:
            f.write(toc_content)
    return doclist
