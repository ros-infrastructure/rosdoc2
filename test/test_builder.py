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

"""testing of builder.py using pytest."""

import argparse
from html.parser import HTMLParser
import logging
import pathlib
from urllib.parse import urlparse

import pytest
from rosdoc2.verbs.build.impl import main_impl, prepare_arguments

logger = logging.getLogger('test-builder')
DATAPATH = pathlib.Path('test/packages')


@pytest.fixture(scope='session')
def session_dir(tmp_path_factory):
    tmp_path_factory.mktemp('build', False)
    tmp_path_factory.mktemp('cross_references', False)
    tmp_path_factory.mktemp('output', False)
    return tmp_path_factory.getbasetemp()


class htmlParser(HTMLParser):
    """Minimal html parsing collecing links and content."""

    def __init__(self):
        super().__init__()
        # data we have seen
        self.content = set()
        # href in <a> tags we have seen
        self.links = set()

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for (name, link) in attrs:
                if name == 'href':
                    self.links.add(link)

    def handle_data(self, data):
        data_black = data.strip(' \n')
        if data_black:
            self.content.add(data_black.lower())


def do_build_package(package_path, work_path) -> None:
    build_dir = work_path / 'build'
    output_dir = work_path / 'output'
    cr_dir = work_path / 'cross_references'

    # Create a top level parser
    parser = prepare_arguments(argparse.ArgumentParser())
    options = parser.parse_args([
        '-p', str(package_path),
        '-c', str(cr_dir),
        '-o', str(output_dir),
        '-d', str(build_dir),
    ])
    logger.info(f'*** Building package(s) at {package_path} with options {options}')

    # run rosdoc2 on the package
    main_impl(options)


def do_test_package(
    name,
    work_path,
    includes=[],
    excludes=[],
    file_includes=[],
    file_excludes=[],
    links_exist=[],
) -> None:
    """Test that package documentation exists and includes/excludes certain text.

    :param pathlib.Path work_path: path where generated files were placed
    :param list[str] includes: lower case text found in index.html data
    :param list[str] excludes: lower case text not found in index.html data
    :param list[str] file_includes: path to files
        (relative to root index.html directory) of files that should exist
    :param list[str] file_excludes: path to files
        (relative to root index.html directory) of files that should not exist
    :param list[str] links_exist: Confirm that 1) a link exists containing this text, and
        2) the link is a valid file
    """
    logger.info(f'*** Testing package {name} work_path {work_path}')
    output_dir = work_path / 'output'

    # tests on the main index.html
    index_path = output_dir / name / 'index.html'

    # smoke test
    assert index_path.is_file(), \
        'html index file exists'

    # read and parse the index file
    #
    # The package title html has a permalink icon at the end which is
    # a unicode character. For some reason, on Windows this character generates
    # a unicode error in Windows, though it seems to work fine
    # in the browser. So ignore unicode errors.
    with index_path.open(mode='r', errors='replace') as f:
        index_content = f.read()
    assert len(index_content) > 0, \
        'index.html is not empty'

    parser = htmlParser()
    parser.feed(index_content)
    logger.debug('HTML text content: ' + str(parser.content))
    logger.debug('HTML <a> tag links: ' + str(parser.links))
    # test inclusions
    for item in includes:
        assert item.lower() in parser.content, \
            f'html should have content <{item}>'

    # test exclusions
    for item in excludes:
        assert item.lower() not in parser.content, \
            f'html should not have content <{item}>'

    # file inclusions
    for item in file_includes:
        path = output_dir / name / item
        assert path.is_file(), \
            f'file <{item}> should exist'

    # file exclusions
    for item in file_excludes:
        path = output_dir / name / item
        assert not path.is_file(), \
            f'file <{item}> should not exist'

    # look for links
    for item in links_exist:
        found_item = None
        for link in parser.links:
            if item in link:
                found_item = link
        assert found_item, \
            f'a link should exist containing the string <{item}>'
        link_object = urlparse(found_item)
        link_path = output_dir / name / link_object.path
        assert link_path.is_file(), \
            f'file represented by <{found_item}> should exist at <{link_path}>'


def test_minimum_package(session_dir):
    """Tests of a package containing as little as possible."""
    PKG_NAME = 'minimum_package'
    do_build_package(DATAPATH / PKG_NAME, session_dir)

    includes = [
        PKG_NAME,
    ]
    excludes = [
        'classes and structs',  # only found in C++ projects
    ]
    file_includes = [
        'search.html',
    ]
    file_excludes = [
        'generated/index.html',  # empty packages have no generated content
    ]
    links_exist = [
        'genindex.html',
    ]
    do_test_package(PKG_NAME, session_dir,
                    includes=includes,
                    excludes=excludes,
                    file_includes=file_includes,
                    file_excludes=file_excludes,
                    links_exist=links_exist)


def test_full_package(session_dir):
    """Test a package with C++, python, and docs."""
    PKG_NAME = 'full_package'
    do_build_package(DATAPATH / PKG_NAME, session_dir)

    includes = [
        PKG_NAME,
        'python api',
        'c++ api',
        'message definitions',
        'service definitions',
        'action definitions'
    ]
    file_includes = [
        'generated/index.html'
    ]
    links_exist = [
        'full_package.dummy.html',
        'modules.html',
    ]
    do_test_package(PKG_NAME, session_dir,
                    includes=includes,
                    file_includes=file_includes,
                    links_exist=links_exist)


def test_only_python(session_dir):
    """Test a pure python package."""
    PKG_NAME = 'only_python'
    do_build_package(DATAPATH / PKG_NAME, session_dir)

    includes = [
        PKG_NAME,
    ]
    links_exist = ['only_python.python_node.html']
    do_test_package(PKG_NAME, session_dir,
                    includes=includes,
                    links_exist=links_exist)


def test_only_messages(session_dir):
    """Test a package only containing messages."""
    PKG_NAME = 'only_messages'

    do_build_package(DATAPATH / PKG_NAME, session_dir)

    includes = [
        PKG_NAME,
        'message definitions',
    ]
    links_exist = ['generated/msg/NumPwrResult.html']

    do_test_package(PKG_NAME, session_dir, includes=includes, links_exist=links_exist)
