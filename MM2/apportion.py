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

    Some supporting resources:
    https://www.census.gov/topics/public-sector/congressional-apportionment/about/computing.html

    https://www2.census.gov/programs-surveys/decennial/2010/data/apportionment/PriorityValues2010.xls
    https://www2.census.gov/programs-surveys/decennial/2010/data/apportionment/PriorityValues2010.pdf <<< logging

    """

    def __init__(self, census, verbose=False):
        self._census = census
        self._verbose = verbose

        self.reps = {}

        # Assign one seat to each state
        for xx in STATES:
            self.reps[xx] = 1
        self.nAssigned = 50

        self._make_priority_queue()

    def assign_next(self, xx):
        """
        Assign the next seat to the state with the highest priority value.
        """
        pass

    ### HELPERS ###

    def _priority_value(self, pop, nSeat):
        pv = pop / math.sqrt(nSeat * (nSeat - 1))

        # TODO: Figure out how floats should be converted to ints here.

        return int(pv)

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
