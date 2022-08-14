#!/usr/bin/env python3
#
# CONGRESSIONAL APPORTIONMENT
#

import math
from .settings import *


class HH_Apportioner:
    """
    Apportionment of US House of Representatives to states.

    See "Calculating Apportionment" in:
    https://www.census.gov/content/dam/Census/library/publications/2011/dec/c2010br-08.pdf

    The algorithm is the Huntington-Hill method:
    https://electionscience.org/library/congressional-apportionment-huntington-hill-method/
    https://en.wikipedia.org/wiki/Huntington%E2%80%93Hill_method

    """

    def __init__(self, census, verbose=False):
        self._census = census
        self.nAssigned = 0
        self._queue = []
        self._verbose = verbose

        self.reps = {}

    def assign_next(self):
        """
        Assign the next seat to the state with the highest priority value.

        Note: The first 50 seats must already be assigned, by calling assign_N().
        """

        assert self.nAssigned >= 50

        n = self.nAssigned - 50
        xx = self._queue[n]["XX"]
        pv = self._queue[n]["PV"]

        self.reps[xx] += 1
        self.nAssigned += 1

        return (self.nAssigned, pv, xx, self.reps[xx])

    def assign_N(self, N):
        """
        Assign seats 1–N (N > 50).
        """

        for xx in STATES:
            self.reps[xx] = 1
        self.nAssigned = 50

        self._make_priority_queue()

        if self._verbose:
            print("HOUSE SEAT,PRIORITY VALUE,STATE ABBREVIATION,STATE SEAT")

        for i in range(51, N + 1):
            hs, pv, xx, ss = self.assign_next()

            if self._verbose:
                print("{},{},{},{}".format(hs, pv, xx, ss))

    def queue_is_ok(self):
        """
        All states still have priority values in the queue.
        """

        remaining_pvs = set()
        n = self.nAssigned - 50
        for row in self._queue[n:]:
            remaining_pvs.add(row["XX"])

        return len(remaining_pvs) == 50

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

        for state in self._census:
            for i in range(2, MAX_SEATS + 1):
                pv = self._priority_value(state["Population"], i)
                self._queue.append({"XX": state["XX"], "PV": pv})

        self._queue = sorted(self._queue, key=lambda x: x["PV"], reverse=True)
