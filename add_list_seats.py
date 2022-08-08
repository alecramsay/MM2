#!/usr/bin/env python3
#
# ADD LIST SEATS FOR THE 2012 ELECTION
#

from MM2 import *


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
    Vf = state["DEM_V"] / (state["REP_V"] + state["DEM_V"])
    Sf = state["DEM_S"] / (state["REP_S"] + state["DEM_S"])
    PR = pr_seats(state["REP_S"] + state["DEM_S"], Vf)
    gap = ue_seats(PR, state["DEM_S"])

    scenario = None
    if abs(gap) > 1:
        scenario = "Case 1"
    elif abs(gap) > 0.5:
        scenario = "Case 2"
    else:
        scenario = "Case 3"

    if verbose:
        print(
            "{}: Vf={:.2f}, Sf={:.2f}, PR={}, gap={}, case={}".format(
                state["XX"], Vf, Sf, PR, gap, scenario
            )
        )


### REPLICATE 2010 REAPPORTIONMENT ###


### ADD LIST SEATS FOR THE 2012 ELECTION ###


print()
