#!/usr/bin/env python3
#
# SETTINGS
#

from enum import Enum


EPSILON = 1 / (10**6)


class Party(Enum):
    REP = "REP"
    DEM = "DEM"
    OTH = "OTH"
