# -*- coding: utf-8 -*-

"""Top-level package for planets."""

__author__ = """K.-Michael Aye"""
__email__ = "kmichael.aye@gmail.com"
__version__ = "0.9"

import inspect
from typing import List

from ._planets import *


def get_all_bodies() -> List[str]:
    """
    Get a list of all available planetary bodies.

    Returns:
        List[str]: Alphabetically sorted list of all planetary body names.
    """
    from . import _planets

    # Find all Planet objects in the module
    body_names = []
    for name, obj in inspect.getmembers(_planets):
        if isinstance(obj, _planets.Planet):
            body_names.append(name)

    return sorted(body_names)
