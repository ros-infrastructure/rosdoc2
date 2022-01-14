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
import shutil

logger = logging.getLogger('rosdoc2')


class Builder:
    """Base class for all builders, which just takes care of some boilerplate logic."""

    def __init__(self, builder_name, builder_entry_dictionary, build_context):
        """Construct a new Builder."""
        self.builder_type = builder_name

        if 'name' not in builder_entry_dictionary:
            raise RuntimeError("Error entry without 'name' field found")
        self.name = builder_entry_dictionary['name']

        if 'output_dir' not in builder_entry_dictionary:
            raise RuntimeError("Error entry without 'output_dir' field found")
        self.output_dir = builder_entry_dictionary['output_dir']

        self.builder_entry_dictionary = builder_entry_dictionary
        self.build_context = build_context

    def build(self, *, doc_build_folder, output_staging_directory):
        """
        Abstract method to actually do the build.

        The output_staging_directory parameter may be useful to refer to
        other builder outputs within this builder.
        For example, if sphinx needs the XML output directory for Doxygen.

        :return: the directory where the documentation was built into, should be
            inside the doc_build_folder. Or None if no artifacts were generated.
        """
        raise NotImplementedError('Should be implemented by subclasses of Builder.')

    def move_file(self, *, source, destination, common_suffix, move=True):
        """
        Move a file into the staging directory.

        May be overridden by downstream builders to selectively skip or rename files.
        """
        if os.path.exists(destination):
            raise RuntimeError(
                f"Error integrating output from builder '{self.name} ({self.builder_type})': "
                f"file '{common_suffix}' already exists in destination '{destination}'. "
                'This usually occurs when two builders generate the same file in '
                'the output directory.')
        if move:
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            shutil.move(os.path.abspath(source), os.path.abspath(destination))

    def move_files(self, *, source, destination):
        """
        Move a directory of files into the output staging directory.

        May be overridden by downstream builders to selectively skip or rename files.
        """
        logger.info(
            f"Moving files for '{self.name} ({self.builder_type})' "
            f"from '{source}' into '{destination}'.")
        number_of_files_moved = 0
        for root, dirs, files in os.walk(source):
            for file in files:
                file_to_copy = os.path.relpath(os.path.join(root, file), start=source)
                self.move_file(
                    source=os.path.join(source, file_to_copy),
                    destination=os.path.join(destination, file_to_copy),
                    common_suffix=file_to_copy)
                number_of_files_moved += 1
        logger.info(f'Moved {number_of_files_moved} files.')
        # Remove temporary output.
        shutil.rmtree(source)
