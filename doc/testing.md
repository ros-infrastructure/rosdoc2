# Testing

To install rosdoc2 prerequisites for testing, run (preferably in a virtual environment)
```bash
pip install ---upgrade --editable .[test]
```

After install with the test option, you can run tests (from the rosdoc2 directory) with:
```bash
pytest
```
If you want to see more output, try the ```-rP``` and/or ```--log-level=DEBUG``` option.

To limit to a particular test, for example the test of "full_package", use ```-k full_package```

Combining these as an example, to get detailed output from the full_package test even for
passed tests, run:
```bash
pytest -rP --log-level=DEBUG -k full_package
```

Testing generates files in a temporary directory, typically at `/tmp/pytest-of-USERNAME`
