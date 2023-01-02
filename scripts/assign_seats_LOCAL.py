#!/usr/bin/env python3
#

"""
Assign list seats to parties, based on a LOCAL election.

Options:
- 's' is the total size of the House (600 [default] or 650 or whatever)
- 'l' is the # of guaranteed list seats per state (0 or 1 [default])

For example:

scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 600 -l 1
scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 650 -l 0


For documentation, type:

scripts/assign_seats_LOCAL.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Tuple

from MM2 import *


### MODS FOR LOCAL USE ###

census_root: str = "data/census"
elections_root: str = "/Users/alecramsay/Downloads"


### PARSE ARGUMENTS ###


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Analyze # of seats per state for a census."
    )

    parser.add_argument(
        "-c", "--cycle", default=2020, help="The census cycle (e.g., 2020)", type=int
    )
    parser.add_argument(
        "-e",
        "--election",
        default=2022,
        help="The election year (e.g., 2022)",
        type=int,
    )
    parser.add_argument(
        "-s",
        "--size",
        default=600,
        help="The total size of the House (e.g., 600 or 650)",
        type=int,
    )
    parser.add_argument(
        "-l",
        "--listmin",
        default=1,
        help="The minimum list seats per state (e.g., 0 or 1)",
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
    election: int = args.election
    size: int = args.size
    list_min: int = args.listmin
    verbose: bool = args.verbose

    ### LOAD THE CENSUS ###

    csv_data: str = "{}/{}_census.csv".format(census_root, cycle)
    types: list = [str, str, int]
    census: list = read_typed_csv(csv_data, types)

    ### LOAD THE ELECTION RESULTS ###

    csv_data: str = "{}/Congressional Elections ({}).csv".format(
        elections_root, election
    )
    types = [str] * 3 + [int] * 8 + [float] * 2
    elections: list = read_typed_csv(csv_data, types)

    ### APPORTION NOMINAL & LIST SEATS TO STATES ###

    app: MM2Apportioner = MM2Apportioner(
        census, elections, list_min=list_min, total_seats=size, verbose=verbose
    )
    app.apportion_and_assign_seats()

    ### WRITE THE RESULTS ###

    reps_by_state: str = "results/{}_reps_by_state({},{}).csv".format(
        election, size, list_min
    )
    save_reps_by_state(app.byState, reps_by_state)

    ### REPORT SOME BASIC INFO ###

    report: str = "results/{}_report({},{}).txt".format(election, size, list_min)
    save_report(app, report)


if __name__ == "__main__":
    main()

### END ###
