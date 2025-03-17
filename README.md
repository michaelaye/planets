# planets

[![PyPI Version](https://img.shields.io/pypi/v/planets.svg)](https://pypi.python.org/pypi/planets)
[![Build Status](https://img.shields.io/github/actions/workflow/status/michaelaye/planets/python-package.yml?branch=master)](https://github.com/michaelaye/planets/actions)
[![Documentation Status](https://img.shields.io/github/actions/workflow/status/michaelaye/planets/deploy.yml?branch=master&label=docs)](https://michaelaye.github.io/planets/)
[![Updates](https://pyup.io/repos/github/michaelaye/planets/shield.svg)](https://pyup.io/repos/github/michaelaye/planets/)

Library to provide planetary constants

* Free software: MIT license
* Documentation: https://michaelaye.github.io/planets/

## Package Structure

This package uses modern Python packaging with `pyproject.toml` for configuration and Hatch for build management.
See the changelog file for more information about changes.

* Version: 0.9
* Python 3.7+ compatible

## Development with Hatch

This project uses [Hatch](https://hatch.pypa.io/) for build management, testing, and publishing:

```bash
# Install Hatch
pip install hatch

# Activate development environment
hatch shell

# Run tests
hatch run test:pytest

# Build package
hatch build

# Install in development mode
pip install -e .
```

## Features

* Provides planetary constants for all major solar system bodies
* Includes complete radii information from SPICE PCK kernels
* Easy access to body properties by name or NAIF ID

## API Usage

You can access planetary data programmatically in your Python code:

```python
# Import specific planets
from planets import Earth, Mars, Jupiter

# Access planetary properties
print(f"Earth's radius: {Earth.R} meters")
print(f"Mars' gravity: {Mars.g} m/s²")
print(f"Jupiter's sidereal length of year [s]: {Jupiter.year} seconds")

# Get list of all available bodies (new helper function)
from planets import get_all_bodies

available_bodies = get_all_bodies()
print(f"Available bodies: {available_bodies}")

# Retrieve body attributes with units
radius_km = Earth.R / 1000
orbit_years = Earth.year / (365.25 * 24 * 3600)
print(f"Earth's radius: {radius_km:.1f} km")
print(f"Earth's orbital period: {orbit_years:.2f} years")
```

## Command Line Interface

The package includes a command-line interface for quick access to planetary data:

```bash
# List all available planetary bodies
planets --list

# Show all attributes for a specific body with units
planets --body Earth

# Show version information
planets --version

# Show help information
planets --help
```

Example output for `planets --body Mars`:

```
Attributes for Mars:
-------------------
S               = 589.2 W/m²
Tsavg           = 210.0 K
Tsmax           = 290.0 K
albedo          = 0.25 fraction
day             = 88775.244147 seconds
eccentricity    = 0.0934
emissivity      = 0.95 fraction
g               = 3.71 m/s²
name            = Mars
obliquity       = 25.19 radians
psurf           = 636.0 Pa
rAU             = 1.52366231 AU
rsm             = 2.27939366e+11 meters
year            = 59354294.4 seconds
```

## Data Sources

Since version 0.6, planetary radii data is read directly from the official NASA SPICE Planetary Constants Kernel (PCK) version 0.11. This ensures that all radius values are consistent with the most widely used planetary constants in the scientific community. The package automatically downloads and parses the necessary SPICE kernel files using the `pooch` library.

SPICE PCK data provides authoritative values for:
- Equatorial radius
- Polar radius
- Mean radius
- Other shape parameters

## Credits

### Planetary Database

Modified by Paul Hayne from the "planets.py" library by Raymond T. Pierrehumbert

Last modified: June, 2017

Sources:

1. http://nssdc.gsfc.nasa.gov/planetary/factsheet/
2. Lang, K. (2012). Astrophysical data: planets and stars. Springer Science & Business Media.    

### Python packaging

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the forked [michaelaye/cookiecutter-pypackage-conda](https://github.com/michaelaye/cookiecutter-pypackage-conda) project template. 