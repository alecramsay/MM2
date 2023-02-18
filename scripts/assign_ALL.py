#!/usr/bin/env python3
#

"""
Assign list seats to parties for all elections

options:
  -c CYCLE, --cycle CYCLE           The census cycle (e.g., 2020)
  -e ELECTION, --election ELECTION  The election year (e.g., 2022)
  -s SIZE, --size SIZE              The total size of the House (e.g., 601 or 651)
  -l LISTMIN, --listmin LISTMIN     The minimum list seats per state (e.g., 0 or 1)
  -v, --verbose                     Verbose mode

For example:

scripts/assign_ALL.py -s 601 -l 1

For documentation, type:

For documentation, type:

scripts/assign_ALL.py -h

"""

import os
import argparse
from argparse import ArgumentParser, Namespace
from typing import List

from MM2 import *


### MODS FOR LOCAL USE ###

census_root: str = "data/census"
elections_root: str = "data/elections"


### PARSE ARGUMENTS ###


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Assign list seats to parties for all elections"
    )

    parser.add_argument(
        "-s",
        "--size",
        default=601,
        help="The total size of the House (e.g., 601 or 651)",
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

    size: int = args.size
    list_min: int = args.listmin
    verbose: bool = args.verbose

    elections: List[int] = list(range(1972, 2022 + 1, 2))

    for election in elections:
        cycle: int = election - ((election - 1) % 10) - 1
        print(
            "Assigning seats for {} ({}), {} seats, {} list min".format(
                election, cycle, size, list_min
            )
        )

        command: str = (
            f"scripts/assign_seats.py -c {cycle} -e {election} -s {size} -l {list_min}"
        )
        os.system(command)


if __name__ == "__main__":
    main()


### END ###
