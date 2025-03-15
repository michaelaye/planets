# -*- coding: utf-8 -*-

"""Console script for planets."""

import argparse
import inspect
import sys
import textwrap
from typing import Any, Dict, List

# Cache the parser to avoid creating it multiple times
_parser = None


def get_all_bodies() -> Dict[str, List[str]]:
    """Get a list of all bodies from the planets module, categorized by type."""
    from planets import get_all_bodies as get_categorized_bodies

    return get_categorized_bodies()


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
        # Skip special methods, private methods, functions, and _R since we show R
        if (
            not name.startswith("__")
            and not name.startswith("_Planet__")
            and not inspect.ismethod(value)
            and not inspect.isfunction(value)
            and name != "_R"  # Skip _R since we show R
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
    global _parser
    if _parser is not None:
        return _parser

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

    _parser = parser
    return parser


def main(args=None):
    """Command-line interface for the planets package."""
    parser = create_parser()
    args = parser.parse_args(args)

    # Process arguments
    if args.version:
        from planets import __version__

        print(f"planets version {__version__}")
        return 0

    elif args.list:
        list_bodies()
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


def list_bodies():
    """List all available planetary bodies."""
    bodies = get_all_bodies()
    print("\nAvailable bodies:")
    for body in bodies:
        print(f"  {body}")
    print()  # Add a blank line at the end


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
