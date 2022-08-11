#!/usr/bin/env python3
#

"""
Add list seats to base congressional apportionment for an election.

For example:

$ scripts/add_list_seats.py

For documentation, type:

$ scripts/add_list_seats.py -h

"""

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
elections = read_typed_csv(csv_data, types)


### APPORTION THE 435 NOMINAL SEATS & ADD LIST SEATS FOR PR ###

app = MM2_Apportioner(census, elections, verbose)
app.eliminate_gap()
