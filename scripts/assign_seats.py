#!/usr/bin/env python3

"""
Assign list seats to parties for an election

options:
  -c CYCLE, --cycle CYCLE           The census cycle (e.g., 2020)
  -e ELECTION, --election ELECTION  The election year (e.g., 2022)
  -s SIZE, --size SIZE              The total size of the House (e.g., 601 or 651)
  -l LISTMIN, --listmin LISTMIN     The minimum list seats per state (e.g., 0 or 1)
  -v, --verbose                     Verbose mode

For example:

scripts/assign_seats.py -c 1970 -e 1972 -s 601 -l 1
scripts/assign_seats.py -c 1980 -e 1982 -s 601 -l 1
scripts/assign_seats.py -c 1990 -e 1992 -s 601 -l 1
scripts/assign_seats.py -c 2000 -e 2002 -s 601 -l 1
scripts/assign_seats.py -c 2010 -e 2012 -s 601 -l 1
scripts/assign_seats.py -c 2020 -e 2022 -s 601 -l 1

For documentation, type:

scripts/assign_seats.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from MM2 import *


### MODS FOR LOCAL USE ###

census_root: str = "data/census"
elections_root: str = "data/elections"


### PARSE ARGUMENTS ###


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Assign list seats to parties for an election"
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
        "-f",
        "--format",
        dest="format",
        action="store_true",
        help="Legacy election format",
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
    legacy: bool = args.format
    verbose: bool = args.verbose

    ### LOAD THE CENSUS ###

    csv_data: str = "{}/{}_census.csv".format(census_root, cycle)
    types: list = [str, str, int]
    census: list = read_csv(csv_data, types)

    ### LOAD THE ELECTION RESULTS ###

    csv_data: str = "{}/Congressional Elections ({}).csv".format(
        elections_root, election
    )
    types = [str] * 3 + [int] * 5 if not legacy else [str] * 3 + [int] * 8 + [float] * 2
    elections: list = read_csv(csv_data, types)

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

    report: str = "results/{}_report({},{}).txt".format(election, size, list_min)
    save_report(app, report)

    summary: str = "results/{}_summary({},{}).csv".format(election, size, list_min)
    save_summary(app, summary)


if __name__ == "__main__":
    main()


### END ###
