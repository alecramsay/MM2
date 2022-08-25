#!/usr/bin/env python3
#

"""
Add list seats to base congressional apportionment for an election.

For example:

$ scripts/MM2_for_Congress.py 2010 2012
$ scripts/MM2_for_Congress.py 2010 2012 -s 2
$ scripts/MM2_for_Congress.py 2010 2012 -s 3 

For documentation, type:

$ scripts/add_reps.py -h

"""

import argparse
from MM2 import *


### PARSE ARGUMENTS ###

parser = argparse.ArgumentParser(
    description="Add MM2 list seats to base congressional apportionment."
)

parser.add_argument("cycle", help="The census cycle (e.g., 2010)", type=int)
parser.add_argument("election", help="The election year (e.g., 2012)", type=int)
parser.add_argument(
    "-s", "--strategy", default=1, help="The list-assignment strategy", type=int
)

parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args = parser.parse_args()

print("strategy: {}".format(args.strategy))


### LOAD THE CENSUS ###

csv_data = "data/census/{}_census.csv".format(args.cycle)
types = [str, str, int]
census = read_typed_csv(csv_data, types)


### LOAD THE ELECTION RESULTS ###

csv_data = "data/elections/Congressional Elections ({}).csv".format(args.election)
types = [str] * 3 + [int] * 8 + [float] * 2
elections = read_typed_csv(csv_data, types)


### APPORTION THE 435 NOMINAL SEATS & ADD LIST SEATS FOR PR ###

app = MM2_Apportioner(census, elections, args.verbose)
app.eliminate_gap(strategy=args.strategy)


### WRITE THE RESULTS ###

write_csv(
    "results/{}_reps_by_state({}).csv".format(args.election, args.strategy),
    [
        {"XX": k, "ANY": v["ANY"], "REP": v["REP"], "DEM": v["DEM"]}
        for k, v in app.reps.items()
    ],
    # rows,
    ["XX", "ANY", "REP", "DEM"],
)
write_csv(
    "results/{}_reps_by_priority({}).csv".format(args.election, args.strategy),
    app.log,
    ["HOUSE SEAT", "PRIORITY VALUE", "STATE", "STATE SEAT", "PARTY", "GAP"],
)


### REPORT SOME BASIC INFO ###

out_path = "results/{}_report({}).txt".format(args.election, args.strategy)
with open(out_path, "w") as f:
    print("{}\n".format(app.baseline), file=f)

    print(
        "{} list seats were added for a total of {}.\n".format(
            app.L, app._base_app.nAssigned
        ),
        file=f,
    )

    if not app.queue_is_ok():
        print(
            "Warning: One or more states have no remaining priority values! Increase MAX_SEATS & re-run.\n",
            file=f,
        )
    else:
        print("All states have remaining priority values.\n", file=f)

    ones = app.one_rep_states()
    if len(ones) > 0:
        print(
            "Some states still have only one representative: {}\n".format(
                ", ".join(ones)
            ),
            file=f,
        )
    else:
        print("All states have more than one representative.\n", file=f)

    unbalanced = app.unbalanced_states()
    if len(unbalanced) > 0:
        print(
            "Some states are still disproportional more than one seat: {}\n".format(
                ", ".join(unbalanced)
            ),
            file=f,
        )
    else:
        print("All states are within one seat of proportional.\n", file=f)