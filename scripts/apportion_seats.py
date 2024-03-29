#!/usr/bin/env python3
#

"""
Apportion nominal & list seats to states based on a census.

For example:

scripts/apportion_seats.py -c 1990 -r 601 -l 1
scripts/apportion_seats.py -c 2000 -r 601 -l 1
scripts/apportion_seats.py -c 2010 -r 601 -l 1
scripts/apportion_seats.py -c 2020 -r 601 -l 1

scripts/apportion_seats.py -c 1990 -r 601 -l 0
scripts/apportion_seats.py -c 2000 -r 601 -l 0
scripts/apportion_seats.py -c 2010 -r 601 -l 0
scripts/apportion_seats.py -c 2020 -r 601 -l 0

For documentation, type:

scripts/apportion_seats.py -h

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
    parser.add_argument("-r", "--reps", default=601, help="The # of reps", type=int)
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
    census: list = read_csv(csv_data, types)

    ### APPORTION NOMINAL & LIST SEATS TO STATES ###

    max_seats: int = 700
    baseapp: HH_Apportioner = HH_Apportioner(census)
    baseapp.log_priority_queue(max_seats)

    app: MM2Apportioner = MM2Apportioner(
        census, list(), list_min=list_min, total_seats=size, verbose=verbose
    )
    app.apportion_seats()

    ### WRITE THE RESULTS ###

    reps_by_priority: str = "results/{}_census_reps_by_priority({}).csv".format(
        args.cycle, max_seats
    )
    save_reps_by_priority(baseapp.byPriority, reps_by_priority)

    reps_by_state: str = "results/{}_census_reps_by_state({},{}).csv".format(
        args.cycle, args.reps, args.listmin
    )
    save_reps_by_state(app.byState, reps_by_state, election_data=False)


if __name__ == "__main__":
    main()

### END ###
