#!/usr/bin/env python3
#
# ADD MM2 LIST SEATS FOR THE 2012 ELECTION
#

from MM2 import *


### ARGS ###

cycle = "2010"
year = "2012"
verbose = True


### LOAD THE CENSUS ###

csv_data = "data/census/{}_census.csv".format(cycle)
types = [str, str, int]
census = read_typed_csv(csv_data, types)


### LOAD THE APPORTIONMENT ###

csv_data = "data/census/Reapportionment for {} Census.csv".format(cycle)
types = [str, str, int]
reps_list = read_typed_csv(csv_data, types)

# Index nominal reps by state XX, along with initialized list reps
# TODO: Move this to the apportioner class
reps = {}
list = {"REP": 0, "DEM": 0}
for state in reps_list:
    reps[state["XX"]] = {"nominal": state["REPS"], "list": list.copy()}

del reps_list


### LOAD THE ELECTION RESULTS ###

csv_data = "data/elections/Congressional Elections ({}).csv".format(year)
types = [str] * 3 + [int] * 8 + [float] * 2
elections_list = read_typed_csv(csv_data, types)

# Index D vote share (fV) & D wins (nS) by state XX
elections = {}
for state in elections_list:
    fV = state["DEM_V"] / (state["REP_V"] + state["DEM_V"])
    nS = state["DEM_S"]
    elections[state["XX"]] = {"fV": fV, "nS": nS}

# Calculate national results

fV, nGap = national_results(elections_list, verbose)

del elections_list


### INITIALIZE THE APPORTIONER ###

app = Apportioner(census, elections, verbose)

pv = app.priority_value(4802982, 2)
pv = app.priority_value(4802982, 3)

# Generate priority values for each state
# Sort them in descending order
# Set the assigned counter to 435

# Replicate the 1990, 2000, 2010, and 2020 apportionments


### ADD LIST SEATS FOR THE 2012 ELECTION ###


print("Done.")
