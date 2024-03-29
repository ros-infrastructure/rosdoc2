# rosdoc2

Command-line tool for generating documentation for ROS 2 packages.

## Quick-start

This tool can be viewed from two perspectives: first from the perspective of a user wanting to building documentation for any given ROS 2 package in order to view it, and second from the perspective of package maintainers who need to write their documentation and configure how this tool works on their package.

### Build documentation for a ROS 2 package

To generate the documentation for almost any ROS 2 package, run this command replacing the arguments with appropriate directories:

```
rosdoc2 build \
  --package-path ./src/path/to/my_package_name
```

> [!NOTE]
> Please see [Known Issues](#known-issues) if failed.

This command will inspect your package and run various documentation tools based on the configuration of your package.

The package directory that you specify must contain a single ROS 2 package that has a `package.xml` file and optionally a YAML configuration file to configure the doc build process.

There will be an `index.html` file in the output directory which you can open manually, or with this command:

```
rosdoc2 open ./doc_output/index.html
```

For more advanced usage see the documentation.

It may be helpful during rosdoc2 development to run a version of rosdoc2 without installing it. This can be done
(after doing an initial normal install to make sure prerequisites are available) by running, from the rosdoc2 main directory:
```bash
python3 -m rosdoc2.main <options>
```

### Set up a ROS 2 package to be used with this tool

In many cases, C/C++ packages require no configuration, and will work if you simply layout your package in a standard configuration and the tool will do the rest.

However, if you want to provide additional documentation, like a conceptual overview or tutorials, then you will want to provide a Sphinx `conf.py` file and do that documentation in `.rst` files using Sphinx.

Additionally, if you have a Python API then you will want to provide a Sphinx `conf.py`

## Installation

### Prerequisite

```
apt install -y python3-pip git
```

and then, install [ros2_documentation](https://github.com/ros2/ros2_documentation?tab=readme-ov-file#prerequisites) required packages.

### `rosdoc2` installation

`rosdoc2` can be installed locally from the git repository.
Clone the repository, change into the directory, and then run:

```
pip install --user --upgrade .
```

`rosdoc2` will be installed under `~/.local/bin/` directory.

## Documentation

The purpose of this tool is to automate the execution of the various documentation tools when building documentation for ROS 2 packages.
Additionally, it provides several out-of-the-box behaviors to minimize configuration in the packages and to provide consistency across packages.

It aims to support two main cases:

- zero configuration generation of C++ and Python API documents with a landing page for simple packages
- custom Doxyfile (for C++) and Sphinx conf.py file for more extensively configured documentation

The goal for the first case is to allow almost no configuration in packages while still providing some useful documentation, even if there is no Doxyfile, Sphinx conf.py file, or any free form documentation.

The goal for the second case is to allow packages to have free form documentation, additional settings for Doxygen and Sphinx, as well as make it possible for developers to easily invoke Doxygen or Sphinx on their projects manually, without this tool.
In this case, the tool would just automate execution of the tools and provide or override certain additional settings to make it more consistent with other packages, for example configuring the output directory or providing the configuration needed to use cross-references via tag files in Doxygen and inventory files in Sphinx.

### Features

Additionally, the tool aims to enable a few features:

- consistent landing page with basic package information for all packages
- support C++ API documentation extraction via Doxygen
- support Python API documentation extraction via Sphinx
- support free form documentation (prose, tutorial, concept pages, etc) via Sphinx
- support cross-language API cross-referencing via Sphinx using Breathe
- support cross-package documentation cross-referencing between packages via Sphinx

### Roadmap Features

Some features were kept in mind while initially developing this tool, but are not yet implemented.
Including:

- extensible "builders", so that other kinds of documentation tools can be supported in the future
- documenting packages without first building them, if the package does not require it
  - packages with generated code, including packages with ROS 2 Messages, need to be built first, but many do not need to be
- using this tool in automated testing and/or CI

### Building Documentation for a Package

### Documenting a Package

What you need to do in order to get basic documentation for your package using this tool is.. nothing.

This tool will extract information from your package's `package.xml` manifest file and generate a landing page for you.

Additionally, if your package is laid out in a standard way then it will automatically run Sphinx and/or Doxygen for you.

However, if you need to place your files in non-standard locations, configure Sphinx and/or Doxygen beyond the defaults, or do something else, you will need to create a `rosdoc2.yaml` file and reference it from your package's `package.xml`.
How to do that, and how to handle some other special cases will follow.

#### Using a `rosdoc2.yaml` file to control how your package is documented

To generate a default config file, run

```
rosdoc2 default_config \
  --package-path ./src/path/to/my_package_name
```

TODO

#### Packages with C/C++ API Documentation

The tool uses information from your package's `package.xml` manifest file, and assumes the source files with documentation to be extracted are all in the `include` folder of your packages, based on the package layout conventions for ROS 2:

https://docs.ros.org/en/rolling/The-ROS2-Project/Contributing/Developer-Guide.html#filesystem-layout

#### Packages with Python API Documentation

TODO

#### Packages with both Python and C/C++ API Documentation

TODO

#### Packages with ROS 2 Messages and other kinds of Interfaces

TODO

### Theory of Operation

It might be helpful, in some cases, to understand how this tool functions.

The tool follows these steps:

- Inspect the `package.xml` of the package for any rosdoc2 specific configurations.
  - Note: if none are found, a default configuration which tries to run Sphinx and Doxygen is used.
  - Note: one of the things that the configuration consists of is build stanzas, each represents an instance of a 'builder' and takes the form of `'output subdir': {<settings>}` and are in the 'builders' key.
    - Note: the 'output subdir' is a relative directory in the output directory specified when running the tool.
- Generate the content for the "package header" which will either be in the package index page (if enabled) or included by the user's Sphinx project.
  - Note: this contains standard information about the package, taken from the package.xml and possibly other sources.
- Generate the documentation. For each builder specified (in order defined):
  - Invoke the builder with the associated settings.
    - Note: each builder is given a separate output directory so file collisions do not occur during doc generation.
  - Attempt to move all files generated into a common output directory.
    - Note: if a file or folder already exists when copying, an error occurs. This is done to catch "file collisions" between the builders, which may otherwise happen silently.
- Generate the package index page, if configured to do so.
- Move the resulting files from the common output directory into the output directory specified by the user.
  - Note: this step can overwrite existing files, e.g. files from a previous run of the tool, but will not delete files that are no longer generated by the documentation, so you may want to delete the output directory if you remove or rename parts of the documentation.

Some things to note from the above:

- Since the key of the builder stanzas is the output directory, it is not possible to have more than one builder run in a single output directory.
- Since builders are run in the order defined, if one builder depends on the output of another, you need to define them in the correct order.

#### Sphinx Builder

The Sphinx builder will attempt to do a few things to ensure it runs even without any configuration:

- If the `sphinx_sourcedir` is provided, it will assert that it exists and use that.
- If not, it will look for a Sphinx project to exist in the conventional `doc` directory in the root of the package.
- If not, it will set up a temporary Sphinx project and run that against the package.

The final default is in place, even for packages with only C++, so that we can enable cross-referencing between packages using Sphinx and Breathe.

If an existing sphinx project is found, the `conf.py` sphinx configuration will be extended to enable rosdoc2-specific features according to the rosdoc2 configuration.
Additionally, the `project`, `author`, `release` and `version` options are populated from package.xml if they are not specified in `conf.py`.

#### Doxygen Builder

The Doxygen builder will attempt to run even with no additional configuration, following these steps:

- If the `doxyfile` setting is provided, it will assert that it exists and use it.
- If not, it will look for a `Doxyfile` in the package's root directory, and use that if it exists.
- If not, it will look for the conventional `include` directory, if it exists it will set up a default Doxygen file and try to document the headers in `include`.

The final default is a best effort to document the headers (assumed to be the public interface for most C++ packages).

## Get in touch

TODO

## Testing

To install rosdoc2 prerequisites for testing, run
```
pip install --user --upgrade .[test]
```

You probably want to test rosdoc2 using code in a local directory rather than
re-running install every time you do a change. To do this, run (from the directory
containing this README):
```
python3 -m pytest
```
If you want to see more output, try the ```-rP``` and/or ```--log-level=DEBUG``` option.
To limit to a particular test, for example the test of "full_package", use ```-k full_package```

Combining these as an example, to get detailed output from the full_package test even for
passed tests, run:
```
python3 -m pytest -rP --log-level=DEBUG -k full_package
```




## Contributing

TODO

## Known Issues

| Description / Error Message | Issue | Workaround |
|:---|:---:|:---|
| `No module named 'rclpy._rclpy_pybind11'` | [#66](https://github.com/ros-infrastructure/rosdoc2/issues/66) | Do not source colcon workspace. |
