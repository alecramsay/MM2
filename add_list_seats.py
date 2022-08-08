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

Vf, Sf, PR, gap = national_results(elections_by_state, verbose)

# - Calculate # proportional seats for each state


### REPLICATE 2010 REAPPORTIONMENT ###


### ADD LIST SEATS FOR THE 2012 ELECTION ###


print()
