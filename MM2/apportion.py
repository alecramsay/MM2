#!/usr/bin/env python3
#
# CONGRESSIONAL APPORTIONMENT
#

import math
from .settings import *


class Apportioner:
    """
    See "Calculating Apportionment" in:
    https://www.census.gov/content/dam/Census/library/publications/2011/dec/c2010br-08.pdf

    The algorithm is the Huntington-Hill method:
    https://electionscience.org/library/congressional-apportionment-huntington-hill-method/
    https://en.wikipedia.org/wiki/Huntington%E2%80%93Hill_method

    Some supporting resources:
    https://www.census.gov/topics/public-sector/congressional-apportionment/about/computing.html
    https://support.ndnfSp.com/portal/en/community/topic/method-of-equal-proportions-from-the-u-s-census
    https://www2.census.gov/programs-surveys/decennial/2010/data/apportionment/PriorityValues2010.pdf

    There is implementation, but it's embedded in a general package and hard to understand & verify:
    https://pypi.org/project/apportionment/
    https://github.com/martinlackner/apportionment

    """

    def __init__(self, census, elections, verbose=False):
        self._census = census
        self._elections = elections
        self._verbose = verbose

        self.reps = {}
        list = {"REP": 0, "DEM": 0}
        for xx in STATES:
            self.reps[xx] = {"nominal": 1, "list": list.copy()}

    def priority_value(self, pop, nSeat):
        pv = pop / math.sqrt(nSeat * (nSeat - 1))

        # TODO: Figure out how floats should be converted to ints here.

        return int(pv)
