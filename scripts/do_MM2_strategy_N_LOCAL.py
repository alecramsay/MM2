#!/usr/bin/env python3
#

"""
Add list seats to the base congressional apportionment for an election.

NOTE - This script allows us to explore various alternative strategies.

NOTE - This is a COPY of do_MM2_strategy_N.py, with the paths to data files NOT in the repo.

For example:

$ scripts/do_MM2_strategy_N_LOCAL.py 2020 2022 -s 7

For documentation, type:

$ scripts/do_MM2_strategy_N_LOCAL.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from MM2 import *

### MODS FOR LOCAL USE ###

census_root: str = "data/census"
elections_root: str = "/Users/alecramsay/Downloads"


### PARSE ARGUMENTS ###

parser: ArgumentParser = argparse.ArgumentParser(
    description="Add MM2 list seats to base congressional apportionment."
)

parser.add_argument("cycle", help="The census cycle (e.g., 2010)", type=int)
parser.add_argument("election", help="The election year (e.g., 2012)", type=int)
parser.add_argument(
    "-s", "--strategy", default=8, help="The list-assignment strategy", type=int
)

parser.add_argument(
    "-r", "--raw", dest="raw", action="store_true", help="Raw elections (not imputed)"
)
parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args: Namespace = parser.parse_args()

print("{}({})|{}".format(args.election, args.strategy, args.cycle))


### LOAD THE CENSUS ###

csv_data = "{}/{}_census.csv".format(census_root, args.cycle)
types: list = [str, str, int]
census: list = read_typed_csv(csv_data, types)


### LOAD THE ELECTION RESULTS ###

csv_data: str = (
    "{}/Congressional Elections ({}).csv".format(elections_root, args.election)
    if args.raw == False
    else "{}/not_imputed/Congressional Elections ({}).csv".format(
        elections_root, args.election
    )
)
types = [str] * 3 + [int] * 8
if args.raw == False:
    types += [float] * 2
elections: list = read_typed_csv(csv_data, types)


### APPORTION THE 435 NOMINAL SEATS & ADD LIST SEATS FOR PR ###

app: MM2_Apportioner = MM2_Apportioner(census, elections, args.verbose)
app.eliminate_gap(strategy=args.strategy)


### WRITE THE RESULTS ###

raw_label: str = "|RAW" if args.raw == True else ""
reps_by_state: str = "results/{}_reps_by_state({}{}).csv".format(
    args.election, args.strategy, raw_label
)
save_reps_by_state(app.byState, reps_by_state)

reps_by_priority: str = "results/{}_reps_by_priority({}{}).csv".format(
    args.election, args.strategy, raw_label
)
save_reps_by_priority(app.byPriority, reps_by_priority)


### REPORT SOME BASIC INFO ###

report: str = "results/{}_report({}{}).txt".format(
    args.election, args.strategy, raw_label
)
save_report(app, report)

### END ###
