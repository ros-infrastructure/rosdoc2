# Copyright 2024 Scott K Logan, R. Kent James
# Licensed under the Apache License, Version 2.0

import argparse
import logging
from pathlib import Path

from colcon_core.location import set_default_config_path
from colcon_core.logging import colcon_logger
from colcon_core.package_discovery import add_package_discovery_arguments
from colcon_core.package_discovery import discover_packages
from colcon_core.package_identification import get_package_identification_extensions


def get_packages(path: str) -> list[object]:
    """Get packages from subdirectories using colcon.

    :parm str path: path to the parent directory to scan for packages
    :return: list of packages

    a package is an object which has package.name, package.type, and package.path

    This function depends on colcon, whose functionality seems to depend on the installed
    extensions. The assumed colcon install should include colcon-common-extensions.
    """
    # colcon global setup
    colcon_logger.setLevel(logging.WARNING)
    set_default_config_path(
        path=(Path('~') / '.colcon').expanduser())

    identification_extensions = get_package_identification_extensions()

    # These discovery arguments could be added to the calling tool's command line
    # or customized implicitly. Either way, the arguments should still be "parsed"
    # because the code expects the default values to be populated.
    parser = argparse.ArgumentParser()
    options = ['--base-paths', path]
    add_package_discovery_arguments(parser)
    args = parser.parse_args(options)

    packages = discover_packages(args, identification_extensions)
    return packages
