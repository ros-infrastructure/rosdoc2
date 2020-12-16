# rosdoc2

Command-line tool for generating documentation for ROS 2 packages.

## Quick-start

To generate the documentation for almost any ROS 2 package, first build the package locally, then run this command:

```
$ rosdoc2 build \
  --build-directory ./build/my_package_name \
  --install-directory ./install \
  --cross-reference-directory ./cross_reference \
  --output-directory ./doc_output \
  --ros-distro foxy \
  ./src/path/to/my_package_name
```

This command will inspect your package and run various documentation tools based on the cofiguration of your package.

The package directory that you specify must contain a single ROS 2 package that has a `package.xml` file and optionally a YAML configuration file to configure the doc build process.

There will be an `index.html` file in the output directory which you can open manually, or with this command:

```
$ rosdoc2 open ./doc_output/index.html
```

For more advanced usage see the documentation.

## Installation

`rosdoc2` is published on PyPI and can be installed from there:

```
$ pip install -U rosdoc2
```

If you wish to install `rosdoc2` for development purposes, refer to the [Contributing](#Contributing) section.

## Documentation

TODO

## Get in touch

TODO

## Testing

TODO

## Contributing

TODO
