## Generated by rosdoc2.verbs.build.builders.SphinxBuilder.
## Based on a recent output from Sphinx-quickstart.

# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# In case this is copied, flake does not like this.
# flake8: noqa

# -- Path setup --------------------------------------------------------------

# rosdoc2 runs sphinx in a wrapping directory so that output does not contaminate
# the source repository. But that can make figuring out the proper path to
# python files tricky in conf.py. Normally you do not have to set this in a custom
# conf.py, as the proper directory is set in a wrapping conf.py (based on the project's
# 'python_source' which by default is the package name). Unfortunately there is no general
# way to do that in a custom conf.py (as it depends on where docs_build is located), so we do
# not recommend sys.path be modified here.
#
# If for some reason you must set a path here, follow this pattern:
#
#import os
#import sys
#sys.path.insert(0, '<absolute path to python source directory>/..')

# -- Project information -----------------------------------------------------

project = 'rclcpp'
ros_distro = os.environ.get('ROS_DISTRO')
if ros_distro:
    project += ': ' + ros_distro.capitalize()

# TODO(tfoote) The docs say year and author but we have this and it seems more relevant.
copyright = 'The <rclcpp> Contributors. License: Apache License 2.0'
author = """Some One"""

# The full version, including alpha/beta/rc tags
release = '0.1.2'

version = '0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
## rosdoc2 will extend the extensions to enable Breathe and Exhale if you
## do not add them here, as well as others, perhaps.
## If you add them manually rosdoc2 may still try to configure them.
## See the rosdoc2_settings below for some options on avoiding that.
extensions = [
    # installed in test installs, but don't install since 'allow_other_extensions' = False
    'sphinx_prompt',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

master_doc = 'index'

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
    '.markdown': 'markdown',
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# In tests, this theme is installed, but will not be used since 'override_theme' = True,
html_theme = 'plone_sphinx_theme'

html_theme_options = {
    # Toc options. The default theme seems to require at least this to be set:
    'collapse_navigation': False,
}

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
rosdoc2_settings = {
    ## This setting, if True, will ensure breathe is part of the 'extensions',
    ## and will set all of the breathe configurations, if not set, and override
    ## settings as needed if they are set by this configuration.
    # 'enable_breathe': True,

    ## This setting, if True, will ensure exhale is part of the 'extensions',
    ## and will set all of the exhale configurations, if not set, and override
    ## settings as needed if they are set by this configuration.
    # 'enable_exhale': True,

    ## This setting, if provided, allows option specification for breathe
    ## directives through exhale. If not set, exhale defaults will be used.
    ## If an empty dictionary is provided, breathe defaults will be used.
    # 'exhale_specs_mapping': {},

    ## This setting, if True, will ensure autodoc is part of the 'extensions'.
    # 'enable_autodoc': True,

    ## This setting, if True, will ensure intersphinx is part of the 'extensions'.
    # 'enable_intersphinx': True,

    ## This setting, if True, will have the 'html_theme' overridden to provide
    ## a consistent style across all of the ROS documentation. If False, will only
    ## override the 'html_theme' if it is not installed.
    # 'override_theme': True,

    ## This setting, if True, will automatically extend the intersphinx mapping
    ## using inventory files found in the cross-reference directory.
    ## If false, the `found_intersphinx_mappings` variable will be in the global
    ## scope when run with rosdoc2, and could be conditionally used in your own
    ## Sphinx conf.py file.
    # 'automatically_extend_intersphinx_mapping': True,

    ## Support markdown
    # 'support_markdown': True,

    ## Allow additional extension. If true, at runtime rosdoc2 will check to see if
    ## non-default extensions are installed, and if so allow them. If false, only
    ## extensions loaded by default by Sphinx or rosdoc2 installs are allowed.
    # 'allow_other_extensions': False,
}
