#!/usr/bin/env python3
#

"""
Find # seats per state at:

- 435 seats 
- 600 seats, and 
- when each state gets 1 more seat after 600

For example:

$ scripts/do_seats_per_state.py --cycle 2020

For documentation, type:

$ scripts/do_seats_per_state.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Tuple

from MM2 import *

### PARSE ARGUMENTS ###


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Analyze # of seats per state for a census."
    )

    parser.add_argument(
        "-c", "--cycle", default=2020, help="The census cycle (e.g., 2020)", type=int
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    args: Namespace = parse_args()
    cycle: int = args.cycle

    ### LOAD THE CENSUS ###

    csv_data: str = "data/census/{}_census.csv".format(cycle)
    types: list = [str, str, int]
    census: list = read_typed_csv(csv_data, types)

    ### TRACK RESULTS BY STATE ###

    by_state: dict = dict()
    for row in census:
        by_state[row["XX"]] = {
            "XX": row["XX"],
            "NAME": row["STATE"],
            "S_435": 0,
            "S_600": 0,
            "S_NEXT": None,
        }

    ### APPORTION NOMINAL SEATS UNTIL EVERY STATE HAS MORE THAN 1 ###

    app: HH_Apportioner = HH_Apportioner(census)

    for xx in STATES:
        app.reps[xx] = 1
        by_state[xx]["S_435"] += 1
        by_state[xx]["S_600"] += 1

    app.N = 50
    single_seats: set[str] = set(STATES)

    app._make_make_priority_queue()

    while single_seats:
        hs: int
        pv: int
        xx: str
        ss: int
        hs, pv, xx, ss = app.assign_next()

        if app.N <= 435:
            by_state[xx]["S_435"] += 1

        if app.N == 435:
            n_single_seats: int = len(single_seats)

        if app.N <= 600:
            by_state[xx]["S_600"] += 1

        single_seats.discard(xx)

        if app.N > 600 and by_state[xx]["S_NEXT"] is None:
            by_state[xx]["S_NEXT"] = app.N

    ### WRITE THE RESULTS ###

    output: list = list()
    for xx, row in by_state.items():
        output.append(row)

    reps_by_census: str = "results/reps_by_census({}).csv".format(cycle)

    write_csv(
        reps_by_census,
        [
            {
                "XX": row["XX"],
                "NAME": row["NAME"],
                "S_435": row["S_435"],
                "S_600": row["S_600"],
                "S_NEXT": row["S_NEXT"],
            }
            for row in output
        ],
        # rows,
        ["XX", "NAME", "S_435", "S_600", "S_NEXT"],
    )

    pass


if __name__ == "__main__":
    main()
