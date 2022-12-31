#!/usr/bin/env python3
#

"""
Generate a priority queue for the HH apportionment algorithm, and
a specific census.

For the 2020 census and 600 reps:
- Two states still have 1 rep -- VT & WY; and
- These are the last two assignments, based on priority:
  599 NY  39
  600 CA  77

For example:

$ scripts/make_priority_queue.py --cycle 2020

For documentation, type:

$ scripts/make_priority_queue.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Tuple

from MM2 import *

### PARSE ARGUMENTS ###


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Generate a priority queue for a census."
    )
    parser.add_argument(
        "-c", "--cycle", default=2020, help="The census cycle (e.g., 2020)", type=int
    )
    parser.add_argument("-r", "--reps", default=600, help="The # of reps", type=int)
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

    ### CREATE THE QUEUE ###

    app: HH_Apportioner = HH_Apportioner(census)

    app._make_make_priority_queue()
    pv_queue: list = app._queue

    ### FIND SEATS BY STATE ###

    by_state: dict = dict()
    for xx in STATES:
        by_state[xx] = 0

    for i, row in enumerate(pv_queue[: args.reps]):
        xx: str = row["XX"]

        by_state[xx] += 1

        if i > (args.reps - 1) - 2:
            print(f"{i+1:3d} {xx} {by_state[xx]:3d}")

    pass

    ### WRITE THE RESULTS ###

    output: list = list()
    for k, v in by_state.items():
        row_out: dict = dict()
        row_out["XX"] = k
        row_out["N'"] = v
        output.append(row_out)

    reps_by_state: str = "results/{}_census_reps_by_state({}).csv".format(
        args.cycle, args.reps
    )

    write_csv(
        reps_by_state,
        [
            {
                "XX": row["XX"],
                "N'": row["N'"],
            }
            for row in output
        ],
        # rows,
        ["XX", "N'"],
    )

    pass


if __name__ == "__main__":
    main()
