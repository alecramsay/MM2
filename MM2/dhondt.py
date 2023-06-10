#!/usr/bin/env python3
#
# The D'Hondt method of apportionment
#

from typing import Tuple


class DHondt_Apportioner:
    """Use the D'Hondt method to apportion seats to parties for an election in a state.

    https://en.wikipedia.org/wiki/D%27Hondt_method
    """

    def __init__(self, N: int, votes: list[dict], verbose=False) -> None:
        self.N: int = N
        self._parties: list = [p["PARTY"] for p in votes]
        self._votes: list[dict] = votes
        self._verbose: bool = verbose

        self._queue: list = list()

        self.reps: dict = {p: 0 for p in self._parties}
        self.byPriority: list = list()

        self._make_make_priority_queue()
        self._assign_seats()

    def baseline(self) -> dict:
        """Return the baseline allocation of seats to parties."""

        return self.reps

    def delta(self, seats: list[dict]) -> dict:
        """Return the +/– delta of seats to parties."""

        self.seats: list[dict] = seats

        delta: dict = {p: (self.reps[p] - self.seats[p]) for p in self._parties}

        return delta

    ### HELPERS ###

    def _make_make_priority_queue(self) -> None:
        """Make a sorted queue of priority values for each party."""

        for party in self._votes:
            for i in range(0, self.N):
                pv: int = quot(party["VOTES"], i)
                self._queue.append({"PARTY": party["PARTY"], "PV": pv})

        self._queue = sorted(self._queue, key=lambda x: x["PV"], reverse=True)

    def _assign_next(self, i: int) -> Tuple[int, int, str, int]:
        """Assign the next seat to the party with the highest priority value."""

        party: str = self._queue[i]["PARTY"]
        pv: int = self._queue[i]["PV"]

        self.reps[party] += 1
        nassigned: int = self.reps[party]

        self.byPriority.append(
            {
                "STATE SEAT": i + 1,
                "PRIORITY VALUE": pv,
                "PARTY": party,
                "PARTY SEAT": nassigned,
            }
        )

        return (i + 1, pv, party, nassigned)

    def _assign_seats(self) -> None:
        """Assign seats to parties"""

        if self._verbose:
            print("STATE SEAT,PRIORITY VALUE,PARTY ABBREVIATION,PARTY SEAT")

        for i in range(self.N):
            ss: int
            pv: int
            party: str
            ps: int
            ss, pv, party, ps = self._assign_next(i)

            if self._verbose:
                print("{},{},{},{}".format(ss, pv, party, ps))


### STANDALONE HELPERS ###


def quot(votes: int, s: int) -> int:
    """D'Hondt quotient - https://en.wikipedia.org/wiki/D%27Hondt_method"""

    return round(votes / (s + 1))


### END ###
