# Copyright 2021 R. Kent James <kent@caspia.com>
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

import os
import subprocess
import tempfile

# projects to test as tuples of (repo_url, project_path)
TEST_PACKAGES = [
    ('https://github.com/rosdabbler/fqdemo.git', 'fqdemo_nodes'),
]
rosdoc2 = os.path.join(os.getcwd(), 'rosdoc2', 'main.py')
def test_smoke_test():
    '''Confirm that rosdoc2 runs to completion in these repos'''
    with tempfile.TemporaryDirectory() as fp:
        for package in TEST_PACKAGES:
            (url, path) = package

            print(f'package url: {url} path: {path}')
            subprocess.run(['git', '-C', f'{fp}', 'clone', f'{url}', 'repo'])
            abs_path = os.path.join(fp, 'repo', path)
            (docs_cr, docs_output, docs_build) = ('docs_cr', 'docs_output', 'docs_build')
            args_str = f"["\
                + '"build"'\
                + f', "-p", "{abs_path}"'\
                + f', "-c", "{os.path.join(abs_path, docs_cr)}"'\
                + f', "-o", "{os.path.join(abs_path, docs_output)}"'\
                + f', "-d", "{os.path.join(abs_path, docs_build)}"'\
                + ']'
            runme = [
                'python',
                '-c', f'from rosdoc2 import main; main.main({args_str})'
            ]
            subprocess.run(runme, check=True, capture_output=True, text=True)
