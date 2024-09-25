# Configuration file for the Sphinx documentation builder.
# This was copied from a generated conf.py, and flake8 does not like it.
# flake8: noqa
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join('/home/kent/github/rkent/rosdoc2/test/packages/basic_cpp/basic_cpp', '..')))


# -- Project information -----------------------------------------------------

project = 'basic_cpp_and_more'
copyright = '2024, Dummy User'
author = 'Custom User'
print('[basic cpp] config.py')

# The full version, including alpha/beta/rc tags
release = '0.0.0'

version = '0.0'


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
    'i_do_not_exist',
    # Shipped with sphinx
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.duration',
    'sphinx.ext.extlinks',
    'sphinx.ext.githubpages',
    'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    'sphinx.ext.imgconverter',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    'sphinx.ext.linkcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    # Sphinx-included math extensions
    'sphinx.ext.imgmath',
    'sphinx.ext.mathjax',

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
## rosdoc2 will override the theme, but you may set one here for running Sphinx
## without the rosdoc2 tool.
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': -1,
    'includehidden': True,
    'titles_only': False,
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
}

## This function is required by the linkcode extension.
## See https://www.sphinx-doc.org/en/master/usage/extensions/linkcode.html
def linkcode_resolve(domain, info):
    return None
