#!/usr/bin/env python3
#
# ADD LIST SEATS FOR THE 2012 ELECTION
#

from MM2 import *

"""
VARIABLES

Per state / election:

National:

"""

### ARGS ###

verbose = True

### LOAD DATA ###

csv_data = "data/census/Reapportionment for 2010 Census.csv"
types = [str, str, int]

reps_by_state = read_typed_csv(csv_data, types)

csv_data = "data/elections/Congressional Elections (2012 - 113th).csv"
types = [str] * 3 + [int] * 8 + [float] * 2

elections_by_state = read_typed_csv(csv_data, types)


### CALCULATE STATE & NATIONAL GAPS ###

nVf, nSf, nPR, nGap = national_results(elections_by_state, verbose)

# Inspect each state's results

for state in elections_by_state:
    party, Vf, Sf, PR, Df, scenario = assign_seat(state, verbose)

    XX = state["XX"]
    Sn = state["DEM_S"]
    N = state["REP_S"] + state["DEM_S"]

    if verbose:
        print(
            "{}: Assign to {} | Sn={:2}, N={:2} Vf={:.4f}, Sf={:.4f}, PR={:2}, Df={:+.4f}, {}".format(
                XX, party, Sn, N, Vf, Sf, PR, Df, scenario
            )
        )


### REPLICATE 2010 REAPPORTIONMENT ###


### ADD LIST SEATS FOR THE 2012 ELECTION ###


print()
