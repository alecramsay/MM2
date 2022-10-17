#!/usr/bin/env python3
#

"""
Add list seats to base congressional apportionment for an election.

For example:

$ scripts/MM2_for_Congress.py 2010 2012
$ scripts/MM2_for_Congress.py 2010 2012 -s 7
$ scripts/MM2_for_Congress.py 2010 2012 -s 7 -r
$ scripts/MM2_for_Congress.py 2000 2006

For documentation, type:

$ scripts/add_reps.py -h

"""

from typing import LiteralString
import argparse
from argparse import ArgumentParser, Namespace

from MM2 import *


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

csv_data: LiteralString = "data/census/{}_census.csv".format(args.cycle)
types: list = [str, str, int]
census: list = read_typed_csv(csv_data, types)


### LOAD THE ELECTION RESULTS ###

csv_data = (
    "data/elections/Congressional Elections ({}).csv".format(args.election)
    if args.raw == False
    else "data/elections/not_imputed/Congressional Elections ({}).csv".format(
        args.election
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

raw_label: LiteralString = "|RAW" if args.raw == True else ""
reps_by_state: str = "results/{}_reps_by_state({}{}).csv".format(
    args.election, args.strategy, raw_label
)

write_csv(
    reps_by_state,
    [
        {
            "XX": k,
            "n": v["n"],
            "v/t": v["v/t"],
            "s": v["s"],
            "SKEW": v["SKEW"],
            "POWER": v["POWER"],
            "n'": v["n'"],
            "s'": v["s'"],
            "SKEW'": v["SKEW'"],
            "POWER'": v["POWER'"],
        }
        for k, v in app.byState.items()
    ],
    # rows,
    ["XX", "n", "v/t", "s", "SKEW", "POWER", "n'", "s'", "SKEW'", "POWER'"],
)

reps_by_priority: LiteralString = "results/{}_reps_by_priority({}{}).csv".format(
    args.election, args.strategy, raw_label
)
write_csv(
    reps_by_priority,
    app.byPriority,
    [
        "HOUSE SEAT",
        "PRIORITY VALUE",
        "STATE",
        "STATE SEAT",
        "Vf",
        "Sf",
        "SKEW|D",
        "SKEW|R",
        "THRESHOLD",
        "PARTY",
        "GAP",
        "SLACK",
    ],
)


### REPORT SOME BASIC INFO ###

report: LiteralString = "results/{}_report({}{}).txt".format(
    args.election, args.strategy, raw_label
)
with open(report, "w") as f:
    print("{}\n".format(app.baseline), file=f)

    print(
        "{} list seats ({} Democratic) were added for a total of {}.\n".format(
            app.N - app.N0,
            app.S - app.S0,
            app._base_app.N,  # Reports the total seats, including "other."
        ),
        file=f,
    )

    if not app.queue_is_ok():
        print(
            "Warning: One or more states have no remaining priority values! Increase MAX_STATE_SEATS & re-run.\n",
            file=f,
        )
    else:
        print("All states have remaining priority values.\n", file=f)

    ones: list = app.one_rep_states()
    if len(ones) > 0:
        print(
            "Some states still have only one representative: {}\n".format(
                ", ".join(ones)
            ),
            file=f,
        )
    else:
        print("All states have more than one representative.\n", file=f)

    unbalanced: list = app.unbalanced_states()
    if len(unbalanced) > 0:
        print(
            "Some states are still disproportional more than one seat: {}\n".format(
                ", ".join(unbalanced)
            ),
            file=f,
        )
    else:
        print("All states are within one seat of proportional.\n", file=f)
