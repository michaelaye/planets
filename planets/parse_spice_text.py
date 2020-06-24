# -*- coding: utf-8 -*-
"""Parses a SPICE text kernel file.
"""

# Copyright 2020, library authors.
#
# Reuse is permitted under the terms of the license.
# The AUTHORS file and the LICENSE file are at the
# top level of this library.

import collections.abc as abc
from pathlib import Path

from astropy import units as u

import pvl


class SPICEparser(pvl.OmniParser):

    def parse_sequence(self, tokens: abc.Generator) -> list:
        # This is really reimplementing _parse_set_seq so that
        # a comma is _NOT_ required between elements of a sequence.
        # since that function is hidden, we have to be explicit.
        # Maybe need to change that?
        delimiters = self.grammar.sequence_delimiters  # convenience
        t = next(tokens)
        if t != delimiters[0]:
            tokens.send(t)
            raise ValueError(f'Expecting a begin delimiter "{delimiters[0]}" '
                             f'but found: "{t}"')
        set_seq = list()
        # Initial WSC and/or empty
        if self.parse_WSC_until(delimiters[1], tokens):
            return set_seq

        # First item:
        set_seq.append(self.parse_value(tokens))
        if self.parse_WSC_until(delimiters[1], tokens):
            return set_seq

        # Remaining items, if any
        while tokens:
            self.parse_WSC_until(None, tokens)  # consume WSC after token
            set_seq.append(self.parse_value(tokens))
            if self.parse_WSC_until(delimiters[1], tokens):
                return set_seq


def parse_tpc(path: Path) -> abc.MutableMapping:
    """Returns a dict-like which contains the variables
    from the SPICE text kernel at *path*.
    """

    tpc_text = path.read_text()

    data_text = get_data(tpc_text)

    # Path("data.tpc").write_text(data_text)

    # SPICE text kernels separate with whitespace, not commas
    tpc_pvl = pvl.loads(data_text, parser=SPICEparser())

    tpc_pvl["file"] = path

    return attach_units(tpc_pvl)


def get_data(s: str) -> str:
    """Returns a string which only contains the 'data' from a SPICE
    text kernel.

    The 'data' parts of a SPICE text kernel are those portions that
    are after a '\begindata' line and before a '\begintext' line
    as the SPICE kernels required reading indicates.
    """
    data = list()
    in_data = False
    for line in s.splitlines():
        if "\\begindata" == line.strip():
            in_data = True
            continue
        if "\\begintext" == line.strip():
            in_data = False
            continue

        if in_data:
            # print(line)
            data.append(line)

    return "\n".join(data)


def attach_units(d: abc.MutableMapping) -> abc.MutableMapping:
    """Returns a dict-like in which some values of *d* are converted
    to astropy.Quantity objects.

    The units are inferred from the key names in *d*.

    Assumes a flat dict-like, does not recurse.
    """
    for k, v in d.items():
        if k.endswith(
            ("N_GEOMAG_CTR_DIPOLE_LON", "N_GEOMAG_CTR_DIPOLE_LAT")
        ):
            d[k] = v * u.deg

        if k.endswith("_RADII"):
            d[k] = v * u.km

        if k.endswith("_GM"):
            d[k] = v * u.km**3 / u.s**2

    return d


