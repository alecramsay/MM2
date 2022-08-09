#!/usr/bin/env python3
#
# ADD MM2 LIST SEATS FOR THE 2012 ELECTION
#

from MM2 import *

"""
VARIABLES - using an amalgam of Hungrarian notation and Camel & Snake Case

Per state / election:

* XX - two-character state abbreviation
* N - # of representatives apportioned to the state

* party - { REP, DEM }
* nS - # of two-party D seats won (whole number)
* fV - two-party D vote share (fraction), unless noted as R
* fS - two-party D seat share (fraction), unless noted as R
* nPR - # of D seats closest to proportional (whole number), given fV
* fD - disproportionality (fraction), fS, nPR, and N
* scenario - { Case 1, Case 2, Case 3 }, for debugging

National:

* fV_Natl - national two-party D vote share (fraction)
* fS_Natl - national two-party D seat share (fraction)
* nPR_Natl - national # of D seats closest to proportional (whole number)
* nGap_Natl - national gap PR and D seats won (whole number)

"""

### ARGS ###

cycle = "2010"
year = "2012"
verbose = True

### LOAD DATA ###


csv_data = "data/census/Reapportionment for {} Census.csv".format(cycle)
types = [str, str, int]
reps = read_typed_csv(csv_data, types)

csv_data = "data/elections/Congressional Elections ({}).csv".format(year)
types = [str] * 3 + [int] * 8 + [float] * 2
elections = read_typed_csv(csv_data, types)


### CALCULATE STATE & NATIONAL GAPS ###

fV_Natl, fS_Natl, nPR_Natl, nGap_Natl = national_results(elections, verbose)

# Inspect each state's results

for state in elections:
    party, fV, fS, nPR, fD, scenario = assign_seat(state, verbose)

    XX = state["XX"]
    nS = state["DEM_S"]
    N = state["REP_S"] + state["DEM_S"]

    if verbose:
        print(
            "{}: Assign to {} | nS={:2}, N={:2} fV={:.4f}, fS={:.4f}, nPR={:2}, Df={:+.4f}, {}".format(
                XX, party, nS, N, fV, fS, nPR, fD, scenario
            )
        )


### REPLICATE 2010 REAPPORTIONMENT ###


### ADD LIST SEATS FOR THE 2012 ELECTION ###


print()
