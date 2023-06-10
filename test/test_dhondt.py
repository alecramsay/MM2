#!/usr/bin/env python3
#
# TEST D'HONDT ALLOCATION
#

import pytest
from MM2 import *


class TestDHondt_Apportioner:
    def test_priority_value(self) -> None:
        """https://en.wikipedia.org/wiki/D%27Hondt_method"""

        N: int = 8
        P: int = 4
        V: int = 230000

        # parties: list = ["A", "B", "C", "D"]
        election: list = [
            {"PARTY": "A", "VOTES": 100000},
            {"PARTY": "B", "VOTES": 80000},
            {"PARTY": "C", "VOTES": 30000},
            {"PARTY": "D", "VOTES": 20000},
        ]
        quotients: list = [
            {"PARTY": "A", "QUOTIENTS": [100000, 50000, 33333, 25000]},
            {"PARTY": "B", "QUOTIENTS": [80000, 40000, 26667, 20000]},
            {"PARTY": "C", "QUOTIENTS": [30000, 15000, 10000, 7500]},
            {"PARTY": "D", "QUOTIENTS": [20000, 10000, 6667, 5000]},
        ]

        for e, q in zip(election, quotients):
            p: str = e["PARTY"]
            v: int = e["VOTES"]

            for s in range(4):
                pv: int = quot(v, s)
                assert pv == q["QUOTIENTS"][s]

    def test_allocation(self) -> None:
        """https://en.wikipedia.org/wiki/D%27Hondt_method"""

        N: int = 8
        P: int = 4
        V: int = 230000

        parties: list = ["A", "B", "C", "D"]
        election: list = [
            {"PARTY": "A", "VOTES": 100000},
            {"PARTY": "B", "VOTES": 80000},
            {"PARTY": "C", "VOTES": 30000},
            {"PARTY": "D", "VOTES": 20000},
        ]
        seats: dict = {"A": 4, "B": 3, "C": 1, "D": 0}

        app: DHondt_Apportioner = DHondt_Apportioner(N, election, verbose=True)

        for p in parties:
            assert app.reps[p] == seats[p]


### END ###
