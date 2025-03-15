# Changelog

All notable changes to this project will be documented in this file.

## [0.7.0] - 2025-03-15

### Changed
- Fully modernized package structure with pyproject.toml
- Replaced multiple tools with Ruff for linting, formatting, and import sorting
- Converted all documentation from RST to Markdown format
- Updated Sphinx configuration to properly support Markdown documentation
- Simplified development dependencies

## [0.6.0] - 2025-03-15

### Added
- Added PCK parser module for extracting constants from SPICE PCK kernel files
- Added functions to retrieve body radii by name
- Added comprehensive NAIF body ID mappings
- Added direct file downloading with pooch package

### Changed
- Modernized package structure using pyproject.toml instead of setup.py/setup.cfg
- Simplified dependency handling, removed unnecessary dependencies
- Converted HISTORY.rst to CHANGELOG.md for better readability
- Updated documentation
- Added support for Python 3.8, 3.9, 3.10, 3.11, and 3.12

## [0.5.0] - 2025-03-14

### Added
- Support for Python 3.12

### Changed
- Updated development dependencies
- Removed spicer from dependencies, using pooch instead for file downloads

## [0.4.6] - 2020-08-29

### Fixed
- Fixed various minor issues

## [0.4.5] - 2019-09-25

### Fixed
- Fixed dependencies

## [0.4.4] - 2019-09-25

### Fixed
- Fixed dependencies

## [0.4.3] - 2019-09-25

### Changed
- Removed requirements.txt, added dependencies in setup

## [0.4.2] - 2019-09-25

### Added
- Added pip requirements

## [0.4.1] - 2019-09-25

### Changed
- Cleaned up notebook

## [0.4.0] - 2019-09-25

### Added
- Added test notebook
- Added example notebook

## [0.3.0] - 2019-06-26

### Added
- Added functionality to get mean radius from SPICE

### Changed
- Applied black formatting rules

## [0.2.0] - 2019-06-26

### Changed
- Changed source of constants to `astropy.constants`

## [0.1.0] - 2019-05-22

### Added
- First release on PyPI 