#!/usr/bin/env python3
#

"""
Analyze the # of seats per state by the total # of seats allocated.

For example:

$ scripts/multiple_seats.py 2020 | grep After

For documentation, type:

$ scripts/multiple_seats.py -h

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

    ### APPORTION NOMINAL SEATS UNTIL EVERY STATE HAS MORE THAN 1 ###

    app: HH_Apportioner = HH_Apportioner(census)

    for xx in STATES:
        app.reps[xx] = 1
    app.N = 50
    single_seats: set[str] = set(STATES)

    app._make_priority_queue()

    print()

    while single_seats:
        hs: int
        pv: int
        xx: str
        ss: int
        hs, pv, xx, ss = app.assign_next()

        single_seats.discard(xx)

        if app.N < 435:
            continue

        if app.N == 435:
            n_single_seats: int = len(single_seats)
            print(
                "After {} seats, {} states have multiple seats: {}".format(
                    app.N, len(single_seats), single_seats
                )
            )
            continue

        if len(single_seats) < n_single_seats:
            n_single_seats = len(single_seats)
            if n_single_seats > 0:
                print(
                    "After {} seats, {} states have multiple seats: {}".format(
                        app.N, len(single_seats), single_seats
                    )
                )

    print(
        "For the {} census, all states have multiple seats after {} seats.".format(
            cycle, app.N
        )
    )


if __name__ == "__main__":
    main()

pass
