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


### APPORTION THE 435 NOMINAL SEATS ###

app = Apportioner(census)
app.assign_435()


### ADD LIST SEATS FOR THE 2012 ELECTION ###

# Initialize the list pool

list_seats = {}
template = {"REP": 0, "DEM": 0}
for xx in STATES:
    list_seats[xx] = template.copy()


print("Done.")
