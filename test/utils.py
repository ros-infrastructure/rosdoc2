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

"""Utilities used in tests."""

from html.parser import HTMLParser
import logging
from urllib.parse import urlparse

logger = logging.getLogger('rosdoc2.test')


class htmlParser(HTMLParser):
    """Minimal html parsing collecting links and content."""

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


def do_test_package(
    name,
    work_dir,
    output_path='output',
    includes=[],
    excludes=[],
    file_includes=[],
    file_excludes=[],
    links_exist=[],
    fragments=[],
) -> htmlParser:
    """Test that package documentation exists and includes/excludes certain text.

    :param pathlib.Path output_dir: path where generated files were placed
    :param str output_path: path relative to work_dir where html files are placed
    :param list[str] includes: lower case text found exactly in index.html data
    :param list[str] excludes: lower case text not found in index.html data
    :param list[str] file_includes: path to files
        (relative to root index.html directory) of files that should exist
    :param list[str] file_excludes: path to files
        (relative to root index.html directory) of files that should not exist
    :param list[str] links_exist: Confirm that 1) a link exists containing this text, and
        2) the link is a valid file
    :param list[str] fragments: lower case text found partially in index.html data
    """
    output_dir = work_dir / output_path
    logger.info(f'*** Testing package {name} output_dir {output_dir}')

    # tests on the main index.html
    index_path = output_dir / name / 'index.html'

    # smoke test
    assert index_path.is_file(), \
        f'html index file exists at {index_path}'

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
        if not item.startswith('http'):
            if item.endswith('/'):
                assert link_path.is_dir(), \
                    f'directory represented by <{item}> ' \
                    f'should exist at <{link_path}>'
            else:
                assert link_path.is_file(), \
                    f'file represented by <{item}> should exist at <{link_path}>'

    # look for fragments of text
    for item in fragments:
        found_fragment = False
        for text in parser.content:
            if item in text:
                found_fragment = True
                break
        assert found_fragment, \
            f'html should have text fragment <{item}>'

    return parser


def do_test_full_package(module_dir, output_path='output', pkg_name='full_package'):
    """Test a package with C++, python, and docs."""
    includes = [
        pkg_name,
        'python api',
        'c++ api',
        'message definitions',
        'service definitions',
        'action definitions',
        'instructions',  # has documentation
        'changelog',
        'full ros2 test package',  # the package description
        'links',
    ]
    file_includes = [
        'generated/index.html'
    ]
    links_exist = [
        f'{pkg_name}.dummy.html',
        'modules.html',
        'doc/morestuff/more_of_more/subsub.html',  # a deep documentation file
        '__standards.html',
        'https://example.com/repo',
        'PACKAGE.html',  # package.xml
    ]
    excludes = [
        'dontshowme'
    ]
    fragments = [
        'this is the package readme.',
    ]
    parser = do_test_package(pkg_name, module_dir,
                             output_path=output_path,
                             includes=includes,
                             file_includes=file_includes,
                             excludes=excludes,
                             links_exist=links_exist,
                             fragments=fragments)

    # We don't want the parent directories to appear
    for item in parser.links:
        assert 'rosdoc2_test_packages' not in item, \
            f'Found link {item} should not contain parent rosdoc2_test_packages'
