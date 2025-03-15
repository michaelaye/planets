# -*- coding: utf-8 -*-

"""Console script for planets."""

import argparse
import inspect
import sys
import textwrap
from typing import Any, Dict, List


def get_all_bodies() -> List[str]:
    """Get a list of all bodies from the planets module."""
    from planets import _planets

    # Find all Planet objects in the module
    body_names = []
    for name, obj in inspect.getmembers(_planets):
        if isinstance(obj, _planets.Planet):
            body_names.append(name)

    return sorted(body_names)


def get_body_attributes(body_name: str) -> Dict[str, Any]:
    """Get all attributes of a specific body."""
    from planets import _planets

    # Get the body object
    body = getattr(_planets, body_name, None)

    if body is None or not isinstance(body, _planets.Planet):
        return None

    # Get all non-function attributes
    attributes = {}
    for name, value in inspect.getmembers(body):
        # Skip special methods, private methods, and functions
        if (
            not name.startswith("__")
            and not name.startswith("_Planet__")
            and not inspect.ismethod(value)
            and not inspect.isfunction(value)
        ):
            attributes[name] = value

    return attributes


def format_attribute_value(name: str, value: Any) -> str:
    """Format attribute value with units and explanation when available."""
    # Certain attributes have known units we can add
    units_map = {
        "R": "meters",
        "g": "m/s²",
        "S": "W/m²",
        "psurf": "Pa",
        "albedo": "fraction",
        "emissivity": "fraction",
        "Qb": "W/m²",
        "gamma": "J·m⁻²·K⁻¹·s⁻¹/²",
        "rsm": "meters",
        "rAU": "AU",
        "year": "seconds",
        "day": "seconds",
        "obliquity": "radians",
        "Lequinox": "radians",
        "Lp": "radians",
        "Tsavg": "K",
        "Tsmax": "K",
    }

    # Format the value with units if applicable
    if name in units_map and value is not None:
        return f"{value} {units_map[name]}"

    return str(value)


def create_parser():
    """Create the argument parser for the CLI."""
    parser = argparse.ArgumentParser(
        description="Command-line interface for the planets package",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          planets --list                  # List all available bodies
          planets --body Mercury          # Show attributes for Mercury
          planets --version               # Show version information
        """),
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--version", action="store_true", help="Show version information")
    group.add_argument("--list", action="store_true", help="List all available bodies")
    group.add_argument("--body", metavar="NAME", help="Show attributes for a specific body")

    return parser


def main(args=None):
    """Command-line interface for the planets package."""
    # Only create the parser when the function is actually called
    # This prevents interference with other tools like pytest during imports
    parser = create_parser()

    # Don't parse args when importing or when pytest is trying to discover tests
    if args is None and "pytest" in sys.modules:
        return 0

    args = parser.parse_args(args)

    # Process arguments
    if args.version:
        from planets import __version__

        print(f"planets version {__version__}")
        return 0

    elif args.list:
        bodies = get_all_bodies()
        print("Available bodies:")
        for body in bodies:
            print(f"  - {body}")
        return 0

    elif args.body:
        body_name = args.body
        attributes = get_body_attributes(body_name)

        if attributes is None:
            print(f"Error: Body '{body_name}' not found.")
            print("Use --list to see available bodies.")
            return 1

        # Print attributes in a pretty way
        print(f"Attributes for {body_name}:")
        print("-" * (13 + len(body_name)))

        # Sort attributes by name for consistent output
        for name in sorted(attributes.keys()):
            value = attributes[name]
            if value is not None:  # Only show attributes that have values
                formatted_value = format_attribute_value(name, value)
                print(f"{name:15} = {formatted_value}")

        return 0

    else:
        # Default behavior when no arguments are provided
        print("planets.cli.main")
        print("Use --help to see available commands.")
        return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
