#!/usr/bin/env python3
#
# CONGRESSIONAL APPORTIONMENT
#

import math
from .settings import *


class Apportioner:
    """
    Apportionment of US House of Representatives to states.

    See "Calculating Apportionment" in:
    https://www.census.gov/content/dam/Census/library/publications/2011/dec/c2010br-08.pdf

    The algorithm is the Huntington-Hill method:
    https://electionscience.org/library/congressional-apportionment-huntington-hill-method/
    https://en.wikipedia.org/wiki/Huntington%E2%80%93Hill_method

    2010 Census & apportionment data:
    https://www.census.gov/data/tables/2010/dec/2010-apportionment-data.html
    https://www2.census.gov/programs-surveys/decennial/2010/data/apportionment/PriorityValues2010.xls
    https://www2.census.gov/programs-surveys/decennial/2010/data/apportionment/PriorityValues2010.pdf <<< log this

    """

    def __init__(self, census, verbose=False):
        self._census = census
        self._verbose = verbose

        self.reps = {}

        # Pre-assign one seat to each state
        for xx in STATES:
            self.reps[xx] = 1
        self._nAssigned = 50

        self._make_priority_queue()

    def assign_next(self):
        """
        Assign the next seat to the state with the highest priority value.
        """

        n = self._nAssigned - 50
        xx = self._queue[n]["XX"]
        pv = self._queue[n]["PV"]

        self.reps[xx] += 1
        self._nAssigned += 1

        if self._verbose:
            print("{},{},{},{}".format(self._nAssigned, pv, xx, self.reps[xx]))

    def assign_435(self):
        """
        Assign seats 50–435.
        """

        if self._verbose:
            print("HOUSE SEAT,PRIORITY VALUE,STATE ABBREVIATION,STATE SEAT")

        for i in range(51, 435 + 1):
            self.assign_next()

    ### HELPERS ###

    def _priority_value(self, pop, nSeat):
        pv = pop / math.sqrt(nSeat * (nSeat - 1))

        # NOTE: By inspection, it appears that rounding is the way that floats are
        # converted to integer priority values.

        return round(pv)

    def _make_priority_queue(self):
        """
        Make a sorted queue of priority values for each state.
        """

        self._queue = []

        for state in self._census:
            for i in range(2, 70 + 1):
                pv = self._priority_value(state["Population"], i)
                self._queue.append({"XX": state["XX"], "PV": pv})

        self._queue = sorted(self._queue, key=lambda x: x["PV"], reverse=True)
