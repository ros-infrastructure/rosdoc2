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

import logging
import os
import sys

from flake8 import LOG
from flake8.api.legacy import get_style_guide


# suppress warning messages from flake8
LOG.setLevel(logging.ERROR)


def test_flake8():
    style_guide = get_style_guide(
        extend_ignore=['D100', 'D104'],
        show_source=True,
    )
    style_guide_tests = get_style_guide(
        extend_ignore=['D100', 'D101', 'D102', 'D103', 'D104', 'D105', 'D107'],
        show_source=True,
    )

    report = style_guide.check_files([
        os.path.join(os.path.dirname(__file__), '..', 'rosdoc2'),
    ])
    report_tests = style_guide_tests.check_files([
        os.path.join(os.path.dirname(__file__), '..', 'test'),
    ])

    total_errors = report.total_errors + report_tests.total_errors
    if total_errors:
        # output summary with per-category counts
        print()
        if report.total_errors:
            report._application.formatter.show_statistics(report._stats)
        if report_tests.total_errors:
            report_tests._application.formatter.show_statistics(
                report_tests._stats)
        print(
            'flake8 reported {total_errors} errors'
            .format_map(locals()), file=sys.stderr)

    assert not total_errors, \
        'flake8 reported {total_errors} errors'.format_map(locals())
