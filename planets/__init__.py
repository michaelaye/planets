# -*- coding: utf-8 -*-

"""Top-level package for planets."""

__author__ = """K.-Michael Aye"""
__email__ = "kmichael.aye@gmail.com"
__version__ = "0.9.1"

from ._planets import *
from ._planets import __all__ as _planets_all

__all__ = _planets_all + ["get_all_bodies"]


def get_all_bodies():
    """Get all planetary bodies defined in the module."""
    # Filter out non-Planet objects and the Planet class from __all__
    return [obj for obj in _planets_all if obj not in ["AU", "sigma", "G", "Planet"]]
