#!/usr/bin/env python3
#
# CONGRESSIONAL APPORTIONMENT
#

import math
from typing import Tuple

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

    def __init__(self, census, verbose=False) -> None:
        self._census = census
        self._queue: list = list()
        self._verbose: bool = verbose

        self.N: int = 0
        self.reps: dict = dict()

    def assign_next(self) -> Tuple[int, int, str, int]:
        """
        Assign the next seat to the state with the highest priority value.

        Note: The first 50 seats must already be assigned, by calling assign_first_N().
        """

        assert self.N >= 50

        n: int = self.N - 50
        xx: str = self._queue[n]["XX"]
        pv: int = self._queue[n]["PV"]

        self.reps[xx] += 1
        self.N += 1

        # HACK - To ensure that all the values of the tuple are explicitly typed.
        N: int = self.N
        nassigned: int = self.reps[xx]

        return (N, pv, xx, nassigned)

    def assign_named(self, xx: str) -> Tuple[int, int, str, int]:
        """
        Assign a seat to the given state, i.e., *not* based on priority value.
        """

        assert self.N >= 50

        pv: int = 0  # HACK - So the data structure is consistent.

        self.reps[xx] += 1
        self.N += 1

        # HACK - To ensure that all the values of the tuple are explicitly typed.
        N: int = self.N
        nassigned: int = self.reps[xx]

        return (N, pv, xx, nassigned)

    def assign_first_N(self, N) -> None:
        """
        Assign seats 1–N (N > 50).
        """

        for xx in STATES:
            self.reps[xx] = 1
        self.N = 50

        self._make_priority_queue()

        if self._verbose:
            print("HOUSE SEAT,PRIORITY VALUE,STATE ABBREVIATION,STATE SEAT")

        for i in range(51, N + 1):
            hs: int
            pv: int
            xx: str
            ss: int
            hs, pv, xx, ss = self.assign_next()

            if self._verbose:
                print("{},{},{},{}".format(hs, pv, xx, ss))

    def queue_is_ok(self) -> bool:
        """
        All states still have priority values in the queue.
        """

        remaining_pvs: set = set()
        n: int = self.N - 50
        for row in self._queue[n:]:
            remaining_pvs.add(row["XX"])

        return len(remaining_pvs) == 50

    ### HELPERS ###

    def _priority_value(self, pop, nSeat) -> int:
        pv: int = round(pop / math.sqrt(nSeat * (nSeat - 1)))

        # NOTE: By inspection, it appears that rounding is the way that floats are
        # converted to integer priority values.

        return pv

    def _make_priority_queue(self) -> None:
        """
        Make a sorted queue of priority values for each state.
        """

        for state in self._census:
            for i in range(2, MAX_STATE_SEATS + 1):
                pv: int = self._priority_value(state["Population"], i)
                self._queue.append({"XX": state["XX"], "PV": pv})

        self._queue = sorted(self._queue, key=lambda x: x["PV"], reverse=True)
