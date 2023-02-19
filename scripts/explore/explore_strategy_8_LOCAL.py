#!/usr/bin/env python3
#

"""
Add list seats to the base congressional apportionment for an election.

This script reflect the final design decisions (Strategy 8) of the many we explored.

NOTE - This is a COPY of do_explore_strategy_N.py, with the paths to data files NOT in the repo.

Run variations of Strategy 8 against LOCAL election data:
- 'a' = allocate 1 seat per state, and then up to 600 (or 650) <<< no list seat guarantee
- 'e' = same as 'a', except guarantee 1 list seat per state with the last few assignments

For example:

scripts/explore_strategy_8_LOCAL.py -c 2020 -e 2022 -s 600 -o a
scripts/explore_strategy_8_LOCAL.py -c 2020 -e 2022 -s 600 -o e


For documentation, type:

scripts/explore_strategy_8_LOCAL.py -h

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

    app: MM2ApportionerSandbox = MM2ApportionerSandbox(census, elections, args.verbose)
    app.list_min: int = list_min
    app.total_seats: int = size
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
    save_reps_by_priority_SANDBOX(app.byPriority, reps_by_priority)

    ### REPORT SOME BASIC INFO ###

    report: str = "results/{}_report({}{},{}).txt".format(
        args.election, strategy, option, size
    )
    save_report(app, report)


if __name__ == "__main__":
    main()

### END ###
