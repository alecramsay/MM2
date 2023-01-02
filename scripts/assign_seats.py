#!/usr/bin/env python3
#

"""
TODO
Assign list seats to parties, based on an election.

Options:
- 'a' = no list seat guarantee
- 'e' = each state guaranteed at least one list seat (from final seats)

For example:

$ scripts/assign_seats.py -c 2020 -e 2022 -s 600 -o a
$ scripts/assign_seats.py -c 2020 -e 2022 -s 600 -o e


For documentation, type:

$ scripts/assign_seats.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Tuple

from MM2 import *


### MODS FOR LOCAL USE ###

census_root: str = "data/census"
elections_root: str = "data/elections"


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
        "-s", "--size", default=600, help="The total size of the House", type=int
    )
    parser.add_argument(
        "-o", "--option", default="a", help="The option: a, b, or c}", type=str
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    args: Namespace = parse_args()

    cycle: int = args.cycle
    strategy: int = 8  # For file names
    size: int = args.size
    option: str = args.option
    list_min: int = 1 if option == "e" else 0

    assert option in ["a", "e"]

    ### LOAD THE CENSUS ###

    csv_data: str = "{}/{}_census.csv".format(census_root, cycle)
    types: list = [str, str, int]
    census: list = read_typed_csv(csv_data, types)

    ### LOAD THE ELECTION RESULTS ###

    csv_data: str = "{}/Congressional Elections ({}).csv".format(
        elections_root, args.election
    )
    types = [str] * 3 + [int] * 8 + [float] * 2
    elections: list = read_typed_csv(csv_data, types)

    ### APPORTION SEATS PER STRATEGY 8 VARIATIONS ###

    # Assign the first 435 seats as they are today

    app: MM2ApportionerSandbox = MM2ApportionerSandbox(
        census, elections, list_min=list_min, total_seats=size, verbose=args.verbose
    )
    app._r: int = 1

    app.strategy8(size=size, option=option)

    ### WRITE THE RESULTS ###

    reps_by_state: str = "results/{}_reps_by_state({}{},{}).csv".format(
        args.election, strategy, option, size
    )
    save_reps_by_state(app.byState, reps_by_state)

    reps_by_priority: str = "results/{}_reps_by_priority({}{},{}).csv".format(
        args.election, strategy, option, size
    )
    save_reps_by_priority(app.byPriority, reps_by_priority)

    ### REPORT SOME BASIC INFO ###

    report: str = "results/{}_report({}{},{}).txt".format(
        args.election, strategy, option, size
    )
    save_report(app, report)


if __name__ == "__main__":
    main()

### END ###
