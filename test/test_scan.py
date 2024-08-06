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

"""testing of builder.py using pytest."""

import argparse
import logging
import pathlib

import pytest
from rosdoc2.verbs.scan.impl import main_impl, prepare_arguments

from .utils import do_test_full_package

logger = logging.getLogger('rosdoc2.test.scan')
DATAPATH = pathlib.Path('test/packages')
OUTPUTPATH = 'scan_output'


@pytest.fixture(scope='module')
def module_dir(tmp_path_factory):
    tmp_path_factory.mktemp('scan_build', False)
    tmp_path_factory.mktemp('scan_cross_references', False)
    tmp_path_factory.mktemp(OUTPUTPATH, False)
    return tmp_path_factory.getbasetemp()


def do_scan_packages(package_path, work_path) -> None:
    build_dir = work_path / 'scan_build'
    output_dir = work_path / OUTPUTPATH
    cr_dir = work_path / 'scan_cross_references'

    # Create a top level parser
    parser = prepare_arguments(argparse.ArgumentParser())
    options = parser.parse_args([
        '-p', str(package_path),
        '-c', str(cr_dir),
        '-o', str(output_dir),
        '-d', str(build_dir),
    ])
    logger.info(f'*** scanning package(s) at {package_path} with options {options}')

    # run rosdoc2 on the package
    main_impl(options)


def test_scan(module_dir):
    """Test a package with C++, python, and docs."""
    output_dir = module_dir / OUTPUTPATH

    do_scan_packages(DATAPATH, module_dir)

    # make sure all packages made output
    for child in DATAPATH.iterdir():
        assert output_dir.joinpath(child.name).is_dir(), \
            f'output directory {output_dir} should have a subdirectory {child.name}'

    do_test_full_package(module_dir, output_path=OUTPUTPATH)
