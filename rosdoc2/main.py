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

import argparse
import sys

from osrf_pycommon.cli_utils.verb_pattern import create_subparsers
from osrf_pycommon.cli_utils.verb_pattern import list_verbs
from osrf_pycommon.cli_utils.verb_pattern import split_arguments_by_verb

COMMAND_NAME = 'rosdoc2'

VERBS_ENTRY_POINT = f'{COMMAND_NAME}.verbs'


def main(sysargs=None):
    """
    Entry point for the command-line interface.

    Mostly boilerplate based on the osrf_pycommon verb pattern documentation.
    """
    # Assign sysargs if not set
    sysargs = sys.argv[1:] if sysargs is None else sysargs

    # Create a top level parser
    parser = argparse.ArgumentParser(
        description=f'{COMMAND_NAME} builds documentation for ROS packages'
    )

    # Generate a list of verbs available
    verbs = list_verbs(VERBS_ENTRY_POINT)

    # Create the subparsers for each verb and collect the arg preprocessors
    argument_preprocessors, verb_subparsers = create_subparsers(
        parser,
        COMMAND_NAME,
        verbs,
        VERBS_ENTRY_POINT,
        sysargs,
    )

    # Determine the verb, splitting arguments into pre and post verb
    verb, pre_verb_args, post_verb_args = split_arguments_by_verb(sysargs)

    # Short circuit -h and --help
    if '-h' in pre_verb_args or '--help' in pre_verb_args:
        parser.print_help()
        sys.exit(0)

    # Error on no verb provided
    if verb is None:
        print(parser.format_usage())
        sys.exit('Error: No verb provided.')
    # Error on unknown verb provided
    if verb not in verbs:
        print(parser.format_usage())
        sys.exit("Error: Unknown verb '{0}' provided.".format(verb))

    # Short circuit -h and --help for verbs
    if '-h' in post_verb_args or '--help' in post_verb_args:
        verb_subparsers[verb].print_help()
        sys.exit(0)

    # First allow the verb's argument preprocessor to strip any args
    # and return any "extra" information it wants as a dict
    processed_post_verb_args, extras = argument_preprocessors[verb](post_verb_args)

    # Then allow argparse to process the left over post-verb arguments along
    # with the pre-verb arguments and the verb itself
    args = parser.parse_args(pre_verb_args + [verb] + processed_post_verb_args)
    # Extend the argparse result with the extras from the preprocessor
    for key, value in extras.items():
        setattr(args, key, value)

    # Finally call the subparser's main function with the processed args
    # and the extras which the preprocessor may have returned
    sys.exit(args.main(args) or 0)


if __name__ == '__main__':
    main()
