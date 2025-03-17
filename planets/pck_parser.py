"""Parser for SPICE PCK kernel files.

This module provides functionality to extract constants from SPICE PCK kernel files
using direct parsing with regular expressions.
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import pooch

# poock automatically caches so this doesn't always download the file
pck_path = pooch.retrieve(
    "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/pck/pck00011.tpc",
    known_hash="sha256:3dff7b1dbeceaa01f25467767d3fa25816051c85d162d1edf04acb310ee28bb1",
)


def extract_data_blocks(pck_content: str) -> List[str]:
    """Extract all data blocks between \begindata and \begintext markers.

    Parameters
    ----------
    pck_content : str
        The content of the PCK file as a string

    Returns
    -------
    List[str]
        List of data blocks extracted from the PCK file
    """
    # Pattern to match blocks between \begindata and \begintext
    pattern = r"\\begindata\s+(.*?)\\begintext"

    # Find all matches with DOTALL to include newlines
    matches = re.findall(pattern, pck_content, re.DOTALL)

    return matches


def parse_data_block(block: str) -> Dict[str, Any]:
    """Parse a single data block using direct regex parsing.

    Parameters
    ----------
    block : str
        A data block extracted from a PCK file

    Returns
    -------
    Dict[str, Any]
        Dictionary of parameters and their values from the data block
    """
    # Remove any leading/trailing whitespace
    block = block.strip()

    # Initialize result dictionary
    result = {}

    # Split into lines
    lines = block.split("\n")

    # Process each line
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines
        if not line:
            i += 1
            continue

        # Look for parameter = value patterns
        # SPICE PCK files typically use NAME = VALUE format
        match = re.match(r"([A-Za-z0-9_]+)\s*=\s*(.*)", line)
        if match:
            key = match.group(1)
            value_str = match.group(2).strip()

            # Handle multi-line values (values ending with parentheses or with continuation lines)
            if "(" in value_str and ")" not in value_str:
                # Collect lines until we find the closing parenthesis
                j = i + 1
                while j < len(lines) and ")" not in lines[j]:
                    value_str += " " + lines[j].strip()
                    j += 1

                # Include the line with the closing parenthesis
                if j < len(lines):
                    value_str += " " + lines[j].strip()
                    i = j  # Update the line index

            # Parse the value
            value = parse_value(value_str)
            result[key] = value

        i += 1

    return result


def parse_value(value_str: str) -> Any:
    """Parse a value from a PCK file.

    Parameters
    ----------
    value_str : str
        String representation of a value

    Returns
    -------
    Any
        Parsed value (float, list, etc.)
    """
    # Remove any leading/trailing whitespace
    value_str = value_str.strip()

    # Handle lists (values in parentheses)
    if value_str.startswith("(") and value_str.endswith(")"):
        # Extract the content inside parentheses
        content = value_str[1:-1].strip()

        # Split by whitespace and parse each element
        elements = re.split(r"\s+", content)

        # Try to convert elements to float
        result = []
        for elem in elements:
            elem = elem.strip()
            if not elem:
                continue

            try:
                # Try parsing as float
                result.append(float(elem))
            except ValueError:
                # If not a number, keep as string
                result.append(elem)

        return result

    # Try to parse as a float
    try:
        return float(value_str)
    except ValueError:
        # Not a number, return as-is
        return value_str


def parse_pck_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Parse a PCK file and extract all constants.

    Parameters
    ----------
    file_path : Union[str, Path]
        Path to the PCK file

    Returns
    -------
    Dict[str, Any]
        Dictionary containing all constants extracted from the PCK file
    """
    file_path = Path(file_path)

    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"PCK file not found: {file_path}")

    # Read the file content
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract data blocks
    blocks = extract_data_blocks(content)

    # Parse each block and combine the results
    all_constants = {}
    for i, block in enumerate(blocks):
        constants = parse_data_block(block)

        # Add block number for debugging/reference
        for key, value in constants.items():
            all_constants[key] = {
                "value": value,
                "block": i + 1,  # 1-based indexing for blocks
            }

    return all_constants


def parse_multiple_files(
    file_paths: List[Union[str, Path]],
) -> Dict[str, Dict[str, Any]]:
    """Parse multiple PCK files and organize the results by file.

    Parameters
    ----------
    file_paths : List[Union[str, Path]]
        List of paths to PCK files

    Returns
    -------
    Dict[str, Dict[str, Any]]
        Dictionary with file names as keys and their parsed constants as values
    """
    results = {}

    for path in file_paths:
        path = Path(path)
        try:
            results[path.name] = parse_pck_file(path)
        except Exception as e:
            print(f"Error parsing {path}: {e}")

    return results


def extract_body_radii(constants: Dict[str, Any]) -> Dict[int, List[float]]:
    """Extract the radii values for all bodies in the constants dictionary.

    Parameters
    ----------
    constants : Dict[str, Any]
        Dictionary of constants parsed from a PCK file

    Returns
    -------
    Dict[int, List[float]]
        Dictionary mapping body IDs to their radii values
    """
    radii_dict = {}

    # Regular expression to match BODY{id}_RADII keys
    radii_pattern = r"BODY(\d+)_RADII"

    for key, data in constants.items():
        match = re.match(radii_pattern, key)
        if match:
            body_id = int(match.group(1))
            # Extract the radii values
            radii_values = data["value"]

            # Handle different formats of radii values
            if isinstance(radii_values, list):
                radii_dict[body_id] = radii_values
            elif isinstance(radii_values, tuple):
                radii_dict[body_id] = list(radii_values)
            else:
                # Try to convert to a list if it's a string representation
                try:
                    # Remove parentheses and split by whitespace
                    values_str = str(radii_values).strip("()[]")
                    radii_list = [float(x) for x in values_str.split()]
                    radii_dict[body_id] = radii_list
                except:
                    print(f"Could not parse radii for body {body_id}: {radii_values}")

    return radii_dict


def get_naif_body_name_mapping() -> Dict[int, str]:
    """Get a dictionary mapping NAIF body IDs to body names.

    This is a comprehensive mapping of NAIF IDs to solar system body names.

    Returns
    -------
    Dict[int, str]
        Dictionary mapping NAIF IDs to body names
    """
    # Define the mapping of NAIF IDs to body names
    # This covers the major bodies in the solar system
    naif_bodies = {
        # Sun and planets
        10: "Sun",
        199: "Mercury",
        299: "Venus",
        399: "Earth",
        499: "Mars",
        599: "Jupiter",
        699: "Saturn",
        799: "Uranus",
        899: "Neptune",
        999: "Pluto",
        # Earth's Moon
        301: "Moon",
        # Mars' moons
        401: "Phobos",
        402: "Deimos",
        # Jupiter's major moons
        501: "Io",
        502: "Europa",
        503: "Ganymede",
        504: "Callisto",
        505: "Amalthea",
        506: "Himalia",
        507: "Elara",
        508: "Pasiphae",
        509: "Sinope",
        510: "Lysithea",
        511: "Carme",
        512: "Ananke",
        513: "Leda",
        514: "Thebe",
        515: "Adrastea",
        516: "Metis",
        # Saturn's major moons
        601: "Mimas",
        602: "Enceladus",
        603: "Tethys",
        604: "Dione",
        605: "Rhea",
        606: "Titan",
        607: "Hyperion",
        608: "Iapetus",
        609: "Phoebe",
        610: "Janus",
        611: "Epimetheus",
        612: "Helene",
        613: "Telesto",
        614: "Calypso",
        615: "Atlas",
        616: "Prometheus",
        617: "Pandora",
        # Uranus' major moons
        701: "Ariel",
        702: "Umbriel",
        703: "Titania",
        704: "Oberon",
        705: "Miranda",
        # Neptune's major moons
        801: "Triton",
        802: "Nereid",
        803: "Naiad",
        804: "Thalassa",
        805: "Despina",
        806: "Galatea",
        807: "Larissa",
        808: "Proteus",
        # Pluto's moons
        901: "Charon",
        902: "Nix",
        903: "Hydra",
        904: "Kerberos",
        905: "Styx",
        # Dwarf planets and large asteroids
        1: "Ceres",
        2: "Pallas",
        3: "Juno",
        4: "Vesta",
        9: "Eris",
        # Comets
        1000012: "67P/Churyumov-Gerasimenko",
        1000036: "Halley",
    }

    return naif_bodies


def get_body_name(body_id: int) -> str:
    """Get the name of a body given its NAIF ID.

    Parameters
    ----------
    body_id : int
        NAIF ID of the body

    Returns
    -------
    str
        Name of the body, or "Unknown" if not found
    """
    naif_mapping = get_naif_body_name_mapping()

    # Check for barycenter IDs
    if body_id % 100 == 0:
        # Barycenter IDs end in 00
        center_id = body_id // 100
        if center_id == 1:
            return "Mercury Barycenter"
        elif center_id == 2:
            return "Venus Barycenter"
        elif center_id == 3:
            return "Earth Barycenter"
        elif center_id == 4:
            return "Mars Barycenter"
        elif center_id == 5:
            return "Jupiter Barycenter"
        elif center_id == 6:
            return "Saturn Barycenter"
        elif center_id == 7:
            return "Uranus Barycenter"
        elif center_id == 8:
            return "Neptune Barycenter"
        elif center_id == 9:
            return "Pluto Barycenter"

    # Return the body name if found, otherwise "Unknown"
    return naif_mapping.get(body_id, f"Unknown ({body_id})")


def get_body_radii_by_name(
    body_name: str, radii_data: Dict[int, List[float]]
) -> Optional[List[float]]:
    """Get the radii for a body by its name.

    Parameters
    ----------
    body_name : str
        Name of the body to retrieve radii for
    radii_data : Dict[int, List[float]]
        Dictionary of body IDs to radii values, typically from extract_body_radii()

    Returns
    -------
    Optional[List[float]]
        List of radii values [equatorial_radius1, equatorial_radius2, polar_radius] if found,
        or None if the body is not found
    """
    # Get the mapping of names to IDs
    naif_mapping = get_naif_body_name_mapping()

    # Create reverse mapping (name to ID)
    name_to_id = {name.lower(): id for id, name in naif_mapping.items()}

    # Convert input name to lowercase for case-insensitive lookup
    body_name_lower = body_name.lower()

    # Try to find the ID for this body name
    body_id = name_to_id.get(body_name_lower)

    if body_id is None:
        # If not found directly, try more flexible matching
        for name, id in name_to_id.items():
            if body_name_lower in name or name in body_name_lower:
                body_id = id
                break

    # If we found an ID, try to get its radii
    if body_id is not None and body_id in radii_data:
        return radii_data[body_id]

    # Special case for Earth's moon - try both "Moon" and "Luna"
    if body_name_lower in ["moon", "luna"] and 301 in radii_data:
        return radii_data[301]

    # Special case for Sun - might be listed under 10
    if body_name_lower == "sun" and 10 in radii_data:
        return radii_data[10]

    return None


def get_body_radius_km(body_name: str, radius_type: str = "mean") -> Optional[float]:
    """Get a specific radius value for a body by name.

    Parameters
    ----------
    body_name : str
        Name of the body
    radius_type : str, optional
        Type of radius to return: "equatorial", "polar", or "mean", by default "mean"

    Returns
    -------
    Optional[float]
        The requested radius in kilometers, or None if not available
    """
    constants = parse_pck_file(pck_path)
    radii_data = extract_body_radii(constants)
    radii = get_body_radii_by_name(body_name, radii_data)

    if radii is None or len(radii) < 3:
        return None

    if radius_type.lower() == "equatorial":
        return radii[0]  # First equatorial radius
    elif radius_type.lower() == "polar":
        return radii[2]  # Polar radius (usually the third value)
    elif radius_type.lower() == "mean":
        # Mean radius is approximately (2*equatorial + polar)/3
        return (2 * radii[0] + radii[2]) / 3
    else:
        raise ValueError(
            f"Unknown radius_type: {radius_type}. Use 'equatorial', 'polar', or 'mean'"
        )
