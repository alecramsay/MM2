#!/usr/bin/env python3
#
# SETTINGS
#

from enum import Enum


EPSILON = 1 / (10**6)


class Party(Enum):
    REP = 1
    DEM = 2
    OTH = 3
