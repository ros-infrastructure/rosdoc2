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
from ..collect_inventory_files import collect_inventory_files
from ..create_format_map_from_package import create_format_map_from_package

logger = logging.getLogger('rosdoc2')

rosdoc2_wrapping_conf_py_template = """\
## Generated by rosdoc2.verbs.build.builders.SphinxBuilder.
## This conf.py imports the user defined (or default if none was provided)
## conf.py, extends the settings to support Breathe and Exhale and to set up
## intersphinx mappings correctly, among other things.

import sys

## exec the user's conf.py to bring all of their settings into this file.
exec(open("{user_conf_py_filename}").read())

def ensure_global(name, default):
    if name not in globals():
        globals()[name] = default

## Based on the rosdoc2 settings, do various things to the settings before
## letting Sphinx continue.

ensure_global('rosdoc2_settings', {{}})
ensure_global('extensions', [])

if rosdoc2_settings.get('enable_autodoc', True):
    print('[rosdoc2] enabling autodoc', file=sys.stderr)
    extensions.append('sphinx.ext.autodoc')

if rosdoc2_settings.get('enable_intersphinx', True):
    print('[rosdoc2] enabling intersphinx', file=sys.stderr)
    extensions.append('sphinx.ext.intersphinx')

if rosdoc2_settings.get('enable_breathe', True):
    # Configure Breathe.
    # Breathe ingests the XML output from Doxygen and makes it accessible from Sphinx.
    print('[rosdoc2] enabling breathe', file=sys.stderr)
    ensure_global('breathe_projects', {{}})
    breathe_projects.update({{
{breathe_projects}}})
    if breathe_projects:
        # Enable Breathe and arbitrarily select the first project.
        extensions.append('breathe')
        breathe_default_project = next(iter(breathe_projects.keys()))

if rosdoc2_settings.get('enable_exhale', True):
    # Configure Exhale.
    # Exhale uses the output of Doxygen and Breathe to create easier to browse pages
    # for classes and functions documented with Doxygen.
    # This is similar to the class hierarchies and namespace listing provided by
    # Doxygen out of the box.
    print('[rosdoc2] enabling exhale', file=sys.stderr)
    extensions.append('exhale')
    ensure_global('exhale_args', {{}})

    from exhale import utils
    exhale_args.update({{
        # These arguments are required.
        "containmentFolder": "{user_sourcedir}/api",
        "rootFileName": "library_root.rst",
        "rootFileTitle": "{package_name} API",
        "doxygenStripFromPath": "..",
        # Suggested optional arguments.
        "createTreeView": True,
        # TIP: if using the sphinx-bootstrap-theme, you need
        # "treeViewIsBootstrap": True,
        "exhaleExecutesDoxygen": False,
        # Maps markdown files to the "md" lexer, and not the "markdown" lexer
        # Pygments registers "md" as a valid markdown lexer, and not "markdown"
        "lexerMapping": {{r".*\.(md|markdown)$": "md",}},
        # This mapping will work when `exhale` supports `:doxygenpage:` directives
        # Check https://github.com/svenevs/exhale/issues/111
        # TODO(aprotyas): Uncomment the mapping below once the above issue is resolved.
        # "customSpecificationsMapping": utils.makeCustomSpecificationsMapping(
        #     lambda kind: [":project:", ":path:", ":content-only:"] if kind == "page" else []),
    }})

if rosdoc2_settings.get('override_theme', True):
    extensions.append('sphinx_rtd_theme')
    html_theme = 'sphinx_rtd_theme'
    print(f"[rosdoc2] overriding theme to be '{{html_theme}}'", file=sys.stderr)

if rosdoc2_settings.get('automatically_extend_intersphinx_mapping', True):
    print(f"[rosdoc2] extending intersphinx mapping", file=sys.stderr)
    if 'sphinx.ext.intersphinx' not in extensions:
        raise RuntimeError(
            "Cannot extend intersphinx mapping if 'sphinx.ext.intersphinx' "
            "has not been added to the extensions")
    ensure_global('intersphinx_mapping', {{
        {intersphinx_mapping_extensions}
    }})

if rosdoc2_settings.get('support_markdown', True):
    print(f"[rosdoc2] adding markdown parser", file=sys.stderr)
    # The `myst_parser` is used specifically if there are markdown files
    # in the sphinx project
    # TODO(aprotyas): Migrate files under the `include` tag in the project's Doxygen
    # configuration into the Sphinx project tree used to run the Sphinx builder in.
    extensions.append('myst_parser')

# if no `primary_domain` option provided, defaults to 'cpp'
if rosdoc2_settings.get('primary_domain', 'cpp'):
    print(f"[rosdoc2] setting primary domain to '{{rosdoc2_settings.get('primary_domain')}}'",
        file=sys.stderr)
    # Tell sphinx what the primary language being documented is.
    primary_domain = rosdoc2_settings.get('primary_domain')

    # Tell sphinx what the pygments highlight language should be.
    highlight_language = rosdoc2_settings.get('primary_domain')
"""

default_conf_py_template = """\
## Generated by rosdoc2.verbs.build.builders.SphinxBuilder.
## Based on a recent output from Sphinx-quickstart.

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = '{package.name}'
# TODO(tfoote) The docs say year and author but we have this and it seems more relevant.
copyright = '2021, {package_licenses}'
author = '{package_authors}'

# The full version, including alpha/beta/rc tags
release = '{package.version}'

version = '{package_version_short}'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
## rosdoc2 will extend the extensions to enable Breathe and Exhale if you
## do not add them here, as well as others, perhaps.
## If you add them manually rosdoc2 may still try to configure them.
## See the rosdoc2_settings below for some options on avoiding that.
extensions = [
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

master_doc = 'index'

source_suffix = {{
    '.rst': 'restructuredtext',
    '.md': 'markdown',
    '.markdown': 'markdown',
}}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
## rosdoc2 will override the theme, but you may set one here for running Sphinx
## without the rosdoc2 tool.
html_theme = 'sphinx_rtd_theme'

html_theme_options = {{
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': -1,
    'includehidden': True,
    'titles_only': False,
}}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
## rosdoc2 comments this out by default because we're not creating it.
# html_static_path = ['_static']

# -- Options for rosdoc2 -----------------------------------------------------

## These settings are specific to rosdoc2, and if Sphinx is run without rosdoc2
## they will be safely ignored.
## None are required by default, so the lines below show the default values,
## therefore you will need to uncomment the lines and change their value
## if you want change the behavior of rosdoc2.
rosdoc2_settings = {{
    ## This setting, if True, will ensure breathe is part of the 'extensions',
    ## and will set all of the breathe configurations, if not set, and override
    ## settings as needed if they are set by this configuration.
    # 'enable_breathe': True,

    ## This setting, if True, will ensure exhale is part of the 'extensions',
    ## and will set all of the exhale configurations, if not set, and override
    ## settings as needed if they are set by this configuration.
    # 'enable_exhale': True,

    ## This setting, if True, will have the 'html_theme' overridden to provide
    ## a consistent style across all of the ROS documentation.
    # 'override_theme': True,

    ## This setting, if True, will automatically extend the intersphinx mapping
    ## using inventory files found in the cross-reference directory.
    ## If false, the `found_intersphinx_mappings` variable will be in the global
    ## scope when run with rosdoc2, and could be conditionally used in your own
    ## Sphinx conf.py file.
    # 'automatically_extend_intersphinx_mapping': True,

    ## Support markdown
    # 'support_markdown': True,

    ## This setting, if set, will attempt to set the `sphinx` options
    ## `primary_domain` and `highlight_language` equal to this setting. These
    ## options allow `sphinx` to choose reasonable defaults for source
    ## code highlighting, among other things.
    ## Possible values (without extensions): 'c', 'cpp', 'js', 'py'
    # 'primary_domain': 'cpp',
}}
"""

index_rst_template = """\
{package.name}
{package_underline}

{package.description}

Package API
===========

.. toctree::
   :maxdepth: 2

   api/library_root
   Full API <api/unabridged_api>
   File structure <api/unabridged_orphan>

Indices and Search
==================

* :ref:`genindex`
* :ref:`search`

"""


class SphinxBuilder(Builder):
    """
    Builder for Sphinx.

    Supported keys for the builder_entry_dictionary include:

    - name (str) (required)
      - name of the documentation, used in reference to the content generated by this builder
    - builder (str) (required)
      - required for all builders, must be 'sphinx' to use this class
    - sphinx_sourcedir (str) (optional)
      - directory containing the Sphinx project, i.e. the `conf.py`, the setting
        you would pass to sphinx-build as SOURCEDIR. Defaults to `doc`.
    """
    def __init__(self, builder_name, builder_entry_dictionary, build_context):
        super(SphinxBuilder, self).__init__(
            builder_name,
            builder_entry_dictionary,
            build_context)

        assert self.builder_type == 'sphinx'

        self.sphinx_sourcedir = None
        self.doxygen_xml_directory = None
        configuration_file_path = build_context.configuration_file_path
        if not os.path.exists(configuration_file_path):
            # This can be the case if the default config is used from a string.
            # Use package.xml instead.
            configuration_file_path = self.build_context.package.filename
        configuration_file_dir = os.path.abspath(os.path.dirname(configuration_file_path))

        # Process keys.
        for key, value in builder_entry_dictionary.items():
            if key in ['name', 'output_dir']:
                continue
            if key == 'sphinx_sourcedir':
                sphinx_sourcedir = os.path.join(configuration_file_dir, value)
                if not os.path.isdir(sphinx_sourcedir):
                    raise RuntimeError(
                        f"Error Sphinx SOURCEDIR '{value}' does not exist relative "
                        f"to '{configuration_file_path}', or is not a directory.")
                self.sphinx_sourcedir = sphinx_sourcedir
            elif key == 'doxygen_xml_directory':
                self.doxygen_xml_directory = value
                # Must check for the existence of this later, as it may not have been made yet.
            else:
                raise RuntimeError(f"Error the Doxygen builder does not support key '{key}'")

        # Prepare the template variables for formatting strings.
        self.template_variables = create_format_map_from_package(build_context.package)

    def build(self, *, doc_build_folder, output_staging_directory):
        # Check that doxygen_xml_directory exists relative to output staging, if specified.
        if self.doxygen_xml_directory is not None:
            self.doxygen_xml_directory = \
                os.path.join(output_staging_directory, self.doxygen_xml_directory)
            self.doxygen_xml_directory = os.path.abspath(self.doxygen_xml_directory)
            if not os.path.isdir(self.doxygen_xml_directory):
                raise RuntimeError(
                    f"Error the 'doxygen_xml_directory' specified "
                    f"'{self.doxygen_xml_directory}' does not exist.")

        # Check if the user provided a sourcedir.
        sourcedir = self.sphinx_sourcedir
        if sourcedir is not None:
            # We do not need to check if this directory exists, as that was done in __init__.
            logger.info(
                f"Note: the user provided sourcedir for Sphinx '{sourcedir}' will be used.")
        else:
            # If the user does not supply a Sphinx sourcedir, check the standard locations.
            standard_sphinx_sourcedir = self.locate_sphinx_sourcedir_from_standard_locations()
            if standard_sphinx_sourcedir is not None:
                logger.info(
                    f"Note: no sourcedir provided, but a Sphinx sourcedir located in the "
                    f"standard location '{standard_sphinx_sourcedir}' and that will be used.")
                sourcedir = standard_sphinx_sourcedir
            else:
                # If the user does not supply a Sphinx sourcedir, and there is no Sphinx project
                # in the conventional location, i.e. '<package dir>/doc', create a temporary
                # Sphinx project in the doc build directory to enable cross-references.
                logger.info(
                    "Note: no sourcedir provided by the user and no Sphinx sourcedir was found "
                    "in the standard locations, therefore using a default Sphinx configuration.")
                sourcedir = os.path.join(doc_build_folder, 'default_sphinx_project')
                self.generate_default_project_into_directory(sourcedir)

        # Collect intersphinx mapping extensions from discovered inventory files.
        inventory_files = \
            collect_inventory_files(self.build_context.tool_options.cross_reference_directory)
        base_url = self.build_context.tool_options.base_url
        intersphinx_mapping_extensions = [
            f"'{package_name}': "
            f"('{base_url}/{package_name}/{inventory_dict['location_data']['relative_root']}', "
            f"'{os.path.abspath(inventory_dict['inventory_file'])}')"
            for package_name, inventory_dict in inventory_files.items()
            # Exclude ourselves.
            if package_name != self.build_context.package.name
        ]

        # Setup rosdoc2 Sphinx file which will include and extend the one in `sourcedir`.
        self.generate_wrapping_rosdoc2_sphinx_project_into_directory(
            doc_build_folder,
            sourcedir,
            intersphinx_mapping_extensions)

        # Invoke Sphinx-build.
        working_directory = doc_build_folder
        sphinx_output_dir = os.path.abspath(os.path.join(doc_build_folder, 'sphinx_output'))
        cmd = [
            'sphinx-build',
            '-c', os.path.relpath(doc_build_folder, start=working_directory),
            os.path.relpath(sourcedir, start=working_directory),
            sphinx_output_dir,
        ]
        logger.info(
            f"Running Sphinx-build: '{' '.join(cmd)}' in '{working_directory}'"
        )
        completed_process = subprocess.run(cmd, cwd=working_directory)
        msg = f"Sphinx-build exited with return code '{completed_process.returncode}'"
        if completed_process.returncode == 0:
            logger.info(msg)
        else:
            raise RuntimeError(msg)

        # Copy the inventory file into the cross-reference directory, but also leave the output.
        inventory_file_name = os.path.join(sphinx_output_dir, 'objects.inv')
        destination = os.path.join(
            self.build_context.tool_options.cross_reference_directory,
            self.build_context.package.name,
            os.path.basename(inventory_file_name))
        logger.info(
            f"Moving inventory file '{inventory_file_name}' into "
            f"cross-reference directory '{destination}'")
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy(
            os.path.abspath(inventory_file_name),
            os.path.abspath(destination)
        )

        # Create a .location.json file as well, so we can know the relative path to the root
        # of the sphinx content from the package's documentation root.
        data = {
            'relative_root': self.output_dir,
        }
        with open(os.path.abspath(destination) + '.location.json', 'w+') as f:
            f.write(json.dumps(data))
        # Put it with the Sphinx generated content as well.
        with open(os.path.abspath(inventory_file_name) + '.location.json', 'w+') as f:
            f.write(json.dumps(data))

        # Return the directory into which Sphinx generated.
        return sphinx_output_dir

    def locate_sphinx_sourcedir_from_standard_locations(self):
        """
        Return the location of a Sphinx project for the package, if one exists
        in a standard location, otherwise None if none are found.

        The standard locations are '<package.xml directory>/doc/source/conf.py' and
        '<package.xml directory>/doc/conf.py', for projects that selected
        "separate source and build directories" when running Sphinx-quickstart and
        those that did not, respectively.
        """
        package_xml_directory = os.path.dirname(self.build_context.package.filename)
        options = [
            os.path.join(package_xml_directory, 'doc'),
            os.path.join(package_xml_directory, 'doc', 'source'),
        ]
        for option in options:
            if os.path.isfile(os.path.join(option, 'conf.py')):
                return option
        return None

    def generate_default_project_into_directory(self, directory):
        os.makedirs(directory, exist_ok=True)

        package = self.build_context.package
        template_variables = {
            'package': package,
            'package_version_short': '.'.join(package.version.split('.')[0:2]),
            'package_licenses': ', '.join(package.licenses),
            'package_authors': ', '.join(set(
                [a.name for a in package.authors] + [m.name for m in package.maintainers]
            )),
            'package_underline': '=' * len(package.name),
        }

        with open(os.path.join(directory, 'conf.py'), 'w+') as f:
            f.write(default_conf_py_template.format_map(template_variables))

        with open(os.path.join(directory, 'index.rst'), 'w+') as f:
            f.write(index_rst_template.format_map(template_variables))

    def generate_wrapping_rosdoc2_sphinx_project_into_directory(
        self,
        directory,
        user_sourcedir,
        intersphinx_mapping_extensions,
    ):
        os.makedirs(directory, exist_ok=True)

        package = self.build_context.package
        breathe_projects = []
        if self.doxygen_xml_directory is not None:
            breathe_projects.append(
                f'        "{package.name} Doxygen Project": "{self.doxygen_xml_directory}"')
        template_variables = {
            'package_name': package.name,
            'user_sourcedir': os.path.abspath(user_sourcedir),
            'user_conf_py_filename': os.path.abspath(os.path.join(user_sourcedir, 'conf.py')),
            'breathe_projects': ',\n'.join(breathe_projects) + '\n    ',
            'intersphinx_mapping_extensions': ',\n        '.join(intersphinx_mapping_extensions)
        }

        print(os.path.abspath(os.path.join(directory, 'conf.py')))
        with open(os.path.join(directory, 'conf.py'), 'w+') as f:
            f.write(rosdoc2_wrapping_conf_py_template.format_map(template_variables))
