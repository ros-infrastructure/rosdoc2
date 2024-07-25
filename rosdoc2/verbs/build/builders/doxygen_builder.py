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

import json
import logging
import os
import shutil
import subprocess

from ..builder import Builder
from ..collect_tag_files import collect_tag_files
from ..create_format_map_from_package import create_format_map_from_package

logger = logging.getLogger('rosdoc2')

DEFAULT_DOXYFILE = """\
## Generated by the rosdoc2.verbs.build.builders.DoxygenBuilder class.

PROJECT_NAME           = {package_name}
PROJECT_NUMBER         = {package_version}
PROJECT_BRIEF          = "{package_description}"

INPUT                  = {package_directory}/include
RECURSIVE              = YES

GENERATE_LATEX         = NO

MACRO_EXPANSION        = YES
EXPAND_ONLY_PREDEF     = YES
STRIP_FROM_PATH        = {package_directory}
"""

EXTENDED_DOXYFILE = """\
## Generated by the rosdoc2.verbs.build.builders.DoxygenBuilder class.

## Include the user defined, or default if none specified, Doxyfile.
@INCLUDE = {doxyfile_file_name}

## Add extra doxyfile statements given by the user.
{extra_doxyfile_statements}

## Add rosdoc2 doxyfile statements for tag files, output directory, etc.
{rosdoc2_doxyfile_statements}
"""


class DoxygenBuilder(Builder):
    """
    Builder for Doxygen.

    Supported keys for the builder_entry_dictionary include:

    - name (str) (required)
      - name of the documentation, used in reference to the content generated by this builder
    - builder (str) (required)
      - required for all builders, must be 'doxygen' to use this class
    - doxyfile (str) (optional)
      - relative path, from the config file, to a Doxyfile to be used instead of the default
    - extra_doxyfile_statements (list[str]) (optional)
      - extra doxyfile statements which would be added after the default, or user, doxyfile
    """

    def __init__(self, builder_name, builder_entry_dictionary, build_context):
        """Construct a new DoxygenBuilder."""
        super(DoxygenBuilder, self).__init__(
            builder_name,
            builder_entry_dictionary,
            build_context)

        assert self.builder_type == 'doxygen'
        self.name = self.name or self.build_context.package.name + ' Public C/C++ API'
        self.output_dir = self.output_dir or 'generated/doxygen'

        # If the build type is not `ament_cmake/cmake`, there is no reason
        # to create a doxygen builder.
        if (
            self.build_context.build_type not in
            ('ament_cmake', 'cmake') and not self.build_context.always_run_doxygen
        ):
            logger.debug(
                f"The package build type is not 'ament_cmake' or 'cmake', hence the "
                f"'{self.builder_type}' builder was not configured")
            return

        self.doxyfile = None
        self.extra_doxyfile_statements = []
        self.rosdoc2_doxyfile_statements = []
        configuration_file_path = build_context.configuration_file_path

        # Process keys.
        for key, value in builder_entry_dictionary.items():
            if key in ['name', 'output_dir']:
                continue
            if key == 'doxyfile':
                config_file_dir = os.path.dirname(configuration_file_path)
                doxyfile = os.path.join(config_file_dir, value)
                if not os.path.exists(doxyfile):
                    raise RuntimeError(
                        f"Error Doxyfile '{value}' does not exist relative "
                        f"to '{configuration_file_path}'")
                self.doxyfile = doxyfile
            elif key == 'extra_doxyfile_statements':
                if not isinstance(value, list):
                    raise RuntimeError(
                        f"Error processing file '{configuration_file_path}', expected setting "
                        f"'extra_doxyfile_statements' to be a list of strings, "
                        f"found '{type(value)}' instead.")
                for statement in value:
                    if not isinstance(statement, str):
                        raise RuntimeError(
                            f"Error processing file '{configuration_file_path}', expected setting "
                            f"'extra_doxyfile_statements' to be a list of strings, "
                            f"found list with type '{type(statement)}' instead.")
                    self.extra_doxyfile_statements.append(statement)
            else:
                raise RuntimeError(f"Error the Doxygen builder does not support key '{key}'")

        # Prepare the template variables for formatting strings.
        self.template_variables = create_format_map_from_package(build_context.package)

        self.doxyfile_content = None
        # If the user does not supply a Doxygen file, look for one in the package root.
        if self.doxyfile is None:
            package_directory = os.path.dirname(build_context.package.filename)
            package_doxyfile = os.path.join(package_directory, 'Doxyfile')
            package_include_directory = os.path.join(package_directory, 'include')
            if os.path.exists(package_doxyfile):
                # In this case, use the package's Doxyfile, despite it not being
                # explicitly specified in the configuration.
                self.doxyfile = package_doxyfile
                logger.info(
                    'No Doxyfile specified by user, but a Doxyfile was found in '
                    f"the package at '{package_doxyfile}' and will be used.")
            elif os.path.isdir(package_include_directory):
                # If neither the doxyfile setting is set,
                # nor is there a Doxyfile in the package root,
                # but there is a standard 'include' directory, then generatate a default.
                self.doxyfile_content = DEFAULT_DOXYFILE.format_map(self.template_variables)
                logger.info(
                    'No Doxyfile specified by user, and no Doxyfile found in '
                    f"the package at '{package_doxyfile}', but a standard include "
                    f"directory was found at '{package_include_directory}', "
                    'therefore a default Doxyfile will be generated and used.')
            else:
                # If neither the doxyfile setting is set,
                # nor is there a Doxyfile in the package root,
                # and there is no standard 'include' directory, then do nothing.
                logger.info(
                    'No Doxyfile specified by user, no Doxyfile found in '
                    f"the package at '{package_doxyfile}', and no standard include "
                    f"directory found at '{package_include_directory}', "
                    'therefore doxygen will not be run.')
        else:
            logger.info(f"Using user specified Doxyfile at '{self.doxyfile}'.")

    def build(self, *, doc_build_folder, output_staging_directory):
        """Actually do the build."""
        # If the build type is not 'ament_cmake/cmake', there is no reason to run doxygen.
        if (
            self.build_context.build_type not in
            ('ament_cmake', 'cmake') and not self.build_context.always_run_doxygen
        ):
            logger.debug(
                f"The package build type is not 'ament_cmake' or 'cmake', hence the "
                f"'{self.builder_type}' builder was not invoked")
            return None  # Explicitly generated no documentation.

        # If both doxyfile and doxyfile_content are None, that means there is
        # no reason to run doxygen.
        if self.doxyfile is None and self.doxyfile_content is None:
            logger.info(
                'Skipping doxygen generation due to lack of configuration and '
                'failure to find code to automatically document.')
            return None  # Explicitly generated no documentation.

        # Create a temporary output directory for doxygen.
        doxygen_output_dir = os.path.abspath(os.path.join(doc_build_folder, 'doxygen_output'))
        os.makedirs(doxygen_output_dir, exist_ok=True)

        # Add the output dir statement to the rosdoc2_doxyfile_statements.
        self.rosdoc2_doxyfile_statements.append(f'OUTPUT_DIRECTORY = {doxygen_output_dir}')

        # Turn on XML generation, so it can be used with Breathe.
        self.rosdoc2_doxyfile_statements.append('GENERATE_XML = YES')

        # Turn on tag file generation and put it into the output directory.
        tag_file_name = os.path.join(doxygen_output_dir, f'{self.build_context.package.name}.tag')
        self.rosdoc2_doxyfile_statements.append(f'GENERATE_TAGFILE = {tag_file_name}')

        # Add entries for tag files found in the cross-reference directory.
        tag_files = collect_tag_files(self.build_context.tool_options.cross_reference_directory)
        base_url = self.build_context.tool_options.base_url
        tag_file_entries = [
            f'TAGFILES += "{os.path.abspath(tagfile_dict["tag_file"])}'
            f'={base_url}/{package_name}/{tagfile_dict["location_data"]["relative_tag_root"]}"'
            for package_name, tagfile_dict in tag_files.items()
            # Exclude ourselves.
            if package_name != self.build_context.package.name
        ]
        self.rosdoc2_doxyfile_statements.extend(tag_file_entries)

        # If the doxyfile has not been specified, generate the default now.
        if self.doxyfile is None:
            assert self.doxyfile_content is not None
            default_doxyfile_path = os.path.join(doc_build_folder, 'Doxyfile.rosdoc2_default')
            with open(default_doxyfile_path, 'w+') as f:
                f.write(self.doxyfile_content)
            self.doxyfile = default_doxyfile_path

        # If the doxyfile is provided by the user, run doxygen in the same directory,
        # so that relative paths, e.g. used for INPUT, still work.
        # Otherwise, use the doc_build_folder.
        working_directory = doc_build_folder
        if self.doxyfile is not None:
            working_directory = os.path.abspath(os.path.dirname(self.doxyfile))

        # Create the "extended" Doxyfile which includes the user (or default) doxyfile.
        extended_doxyfile_path = os.path.join(doc_build_folder, 'Doxyfile.rosdoc2')
        with open(extended_doxyfile_path, 'w+') as f:
            f.write(EXTENDED_DOXYFILE.format_map({
                'doxyfile_file_name': os.path.relpath(
                    self.doxyfile,
                    start=working_directory),
                'extra_doxyfile_statements': '\n'.join(self.extra_doxyfile_statements),
                'rosdoc2_doxyfile_statements': '\n'.join(self.rosdoc2_doxyfile_statements)
            }))

        # Invoke Doxygen.
        cmd = ['doxygen', os.path.relpath(extended_doxyfile_path, start=working_directory)]
        logger.info(
            f"Running Doxygen: '{' '.join(cmd)}' in '{working_directory}'"
        )
        completed_process = subprocess.run(cmd, cwd=working_directory)
        logger.info(
            f"Doxygen exited with return code '{completed_process.returncode}'")

        # Copy the tag file into the cross-reference directory, but also leave it in the output.
        destination = os.path.join(
            self.build_context.tool_options.cross_reference_directory,
            self.build_context.package.name,
            os.path.basename(tag_file_name))
        logger.info(
            f"Moving tag file '{tag_file_name}' into cross-reference directory '{destination}'")
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy(
            os.path.abspath(tag_file_name),
            os.path.abspath(destination)
        )

        # Create a tag.location.json file as well, so we can know the relative path to the root
        # of the doxygen content from the package's documentation root.
        data = {
            'relative_tag_root': os.path.join(self.output_dir, 'html'),
        }
        with open(os.path.abspath(destination) + '.location.json', 'w+') as f:
            f.write(json.dumps(data))
        # Put it with the doxygen generated content as well.
        with open(os.path.abspath(tag_file_name) + '.location.json', 'w+') as f:
            f.write(json.dumps(data))

        # Return the directory into which doxygen generated.
        return doxygen_output_dir
