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
import shutil

logger = logging.getLogger('rosdoc2')

documentation_rst_template = """\
Documentation
=============

.. toctree::
   :maxdepth: 1
   :titlesonly:
   :glob:

   {rel_user_doc_directory}/*
"""

subdirectory_rst_template = """\
{name}/
{name_underline}=

.. toctree::
   :caption: Documentation in this subdirectory
   :maxdepth: 1
   :titlesonly:
   :glob:

   *
"""


def include_user_docs(rel_user_doc_directory: str,
                      output_dir: str,
                      package_xml_directory: str
                      ):
    """Generate rst files for user documents."""
    logger.info(f'include_user_docs: rel_user_doc_directory <{rel_user_doc_directory}> '
                f'output_dir <{output_dir}>')
    user_doc_directory = os.path.join(
        os.path.join(package_xml_directory, rel_user_doc_directory))
    doc_directories = []
    for root, dirs, files in os.walk(user_doc_directory):
        for file in files:
            # ensure a valid documentation file exists, directories might only contain resources.
            (_, ext) = os.path.splitext(file)
            if ext in ['.rst', '.md', '.markdown']:
                logger.debug(f'Found renderable documentation file in {root} named {file}')
                doc_directories.append(os.path.relpath(root, user_doc_directory))
                break
        if 'index.rst' in files:
            # We assume that this index will also show any desired files in subdirectories
            dirs.clear()

    if not doc_directories:
        logger.debug(f'no documentation found in {user_doc_directory}')
        return doc_directories

    logger.info(f'Documentation found in directories {doc_directories}')
    # At this point we know that there are some directories that have documentation in them under
    # /doc, but we do not know which ones might also be needed for images or includes. So we copy
    # everything to the output directory.
    logger.info(f'Copying {os.path.join(package_xml_directory, rel_user_doc_directory)} to '
                f'{os.path.join(output_dir, rel_user_doc_directory)}')
    shutil.copytree(
        os.path.join(package_xml_directory, rel_user_doc_directory),
        os.path.join(output_dir, rel_user_doc_directory),
        dirs_exist_ok=True)

    toc_content = documentation_rst_template.format_map(
        {'rel_user_doc_directory': rel_user_doc_directory})
    # generate a glob rst entry for each directory with documents
    for relpath in doc_directories:
        # files that will be explicitly listed in index.rst
        if relpath == '.':
            continue
        index_path = os.path.join(output_dir, rel_user_doc_directory, relpath, 'index.rst')
        if os.path.isfile(index_path):
            logger.info(f'Using existing index.rst in directory {relpath}')
        else:
            logger.info(f'No index.rst in {relpath}, creating one.')
            content = subdirectory_rst_template.format_map(
                {'name': relpath,
                 'name_underline': '=' * len(relpath)})
            with open(index_path, 'w+') as f:
                f.write(content)
        toc_content += f'   {rel_user_doc_directory}/{relpath}/index\n'

    sub_path = os.path.join(output_dir, 'user_docs.rst')
    with open(sub_path, 'w+') as f:
        f.write(toc_content)

    return doc_directories
