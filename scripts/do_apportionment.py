#!/usr/bin/env python3
#

"""
Apportion nominal & list seats to states based on a census.

For example:

$ scripts/do_apportionment.py --cycle 1990
$ scripts/do_apportionment.py --cycle 2000
$ scripts/do_apportionment.py --cycle 2000
$ scripts/do_apportionment.py --cycle 2020

For documentation, type:

$ scripts/do_apportionment.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Tuple

from MM2 import *

### PARSE ARGUMENTS ###


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Apportion nominal & list seats to states based on a census."
    )
    parser.add_argument(
        "-c", "--cycle", default=2020, help="The census cycle (e.g., 2020)", type=int
    )
    parser.add_argument("-r", "--reps", default=600, help="The # of reps", type=int)
    parser.add_argument(
        "-l",
        "--listmin",
        default=1,
        help="The minimum # of list reps / state",
        type=int,
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    args: Namespace = parse_args()
    cycle: int = args.cycle
    list_min: int = args.listmin
    size: int = args.reps
    verbose: bool = args.verbose

    ### LOAD THE CENSUS ###

    csv_data: str = "data/census/{}_census.csv".format(cycle)
    types: list = [str, str, int]
    census: list = read_typed_csv(csv_data, types)

    ### APPORTION NOMINAL & LIST SEATS TO STATES ###

    app: MM2Apportioner = MM2Apportioner(
        census, None, list_min=list_min, total_seats=size, verbose=verbose
    )
    app.apportion_seats()

    # TODO - DELETE
    # app: HH_Apportioner = HH_Apportioner(census)

    # app._make_make_priority_queue()
    # pv_queue: list = app._queue

    # ### FIND SEATS BY STATE ###

    # by_state: dict = dict()
    # for xx in STATES:
    #     by_state[xx] = {"nominal": 1, "list": 0}
    # N: int = 50

    # no_list_seats: set[str] = set()
    # for xx in STATES:
    #     no_list_seats.add(xx)

    # for i, row in enumerate(pv_queue[: size - 50]):
    #     N += 1
    #     xx: str = row["XX"]

    #     if i < 435:
    #         by_state[xx]["nominal"] += 1
    #     else:
    #         by_state[xx]["list"] += 1
    #         no_list_seats.discard(xx)

    #         if (size - N) == len(no_list_seats):
    #             # Assign the remaining seats to states with no list seats
    #             break

    # # Assign the remaining seats to states with no list seats
    # for xx in no_list_seats:
    #     by_state[xx]["list"] += 1

    ### WRITE THE RESULTS ###

    # TODO - HERE
    output: list = list()
    for k, v in by_state.items():
        row_out: dict = dict()
        row_out["XX"] = k
        row_out["NOMINAL"] = v["nominal"]
        row_out["LIST"] = v["list"]
        output.append(row_out)

    reps_by_state: str = "results/{}_census_reps_by_state({}).csv".format(
        args.cycle, args.reps
    )

    write_csv(
        reps_by_state,
        [
            {
                "XX": row["XX"],
                "NOMINAL": row["NOMINAL"],
                "LIST": row["LIST"],
            }
            for row in output
        ],
        # rows,
        ["XX", "NOMINAL", "LIST"],
    )

    pass


if __name__ == "__main__":
    main()

### END ###
