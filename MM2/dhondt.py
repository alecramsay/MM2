#!/usr/bin/env python3
#
# The D'Hondt method of apportionment
#

import math
from typing import Tuple


class DHondt_Apportioner:
    """Use the D'Hondt method to apportion seats to parties for an election in a state.

    https://en.wikipedia.org/wiki/D%27Hondt_method
    """

    def __init__(self, N: int, election: list[dict], verbose=False) -> None:
        self.N: int = N
        self._election = election
        self._verbose: bool = verbose

        self._queue: list = list()
        self.reps: dict = dict()
        self.byPriority: list = list()

        self._make_make_priority_queue()

    # def assign_first_N(self, N) -> None:
    #     """
    #     Assign seats 1–N (N > 50).
    #     """

    #     for xx in STATES:
    #         self.reps[xx] = 1
    #     self.N = 50

    #     self._make_make_priority_queue()

    #     if self._verbose:
    #         print("HOUSE SEAT,PRIORITY VALUE,STATE ABBREVIATION,STATE SEAT")

    #     for i in range(51, N + 1):
    #         hs: int
    #         pv: int
    #         xx: str
    #         ss: int
    #         hs, pv, xx, ss = self.assign_next()

    #         if self._verbose:
    #             print("{},{},{},{}".format(hs, pv, xx, ss))

    ### HELPERS ###

    # def _priority_value(self, votes: int, s: int) -> int:
    #     pv: int = quot(votes, s)

    #     return pv

    def _make_make_priority_queue(self) -> None:
        """Make a sorted queue of priority values for each party."""

        for party in self._election:
            for i in range(1, self.N + 1):
                pv: int = quot(party["VOTES"], i)
                self._queue.append({"PARTY": party["PARTY"], "PV": pv})

        self._queue = sorted(self._queue, key=lambda x: x["PV"], reverse=True)

    def _assign_next(self) -> Tuple[int, int, str, int]:
        """Assign the next seat to the party with the highest priority value."""

        n: int = self.N
        party: str = self._queue[n]["PARTY"]
        pv: int = self._queue[n]["PV"]

        self.reps[party] += 1
        self.N += 1

        # HACK - To ensure that all the values of the tuple are explicitly typed.
        N: int = self.N
        nassigned: int = self.reps[party]

        self.byPriority.append(
            {
                "STATE SEAT": N,
                "PRIORITY VALUE": pv,
                "PARTY": party,
                "PARTY SEAT": nassigned,
            }
        )

        return (N, pv, party, nassigned)


### STANDALONE HELPERS ###


def quot(votes: int, s: int) -> int:
    """D'Hondt quotient - https://en.wikipedia.org/wiki/D%27Hondt_method"""

    return round(votes / (s + 1))


### END ###
