#!/usr/bin/env python3
#

"""
Add list seats to base congressional apportionment for an election.

For example:

$ scripts/add_list_seats.py 2000 2002 -v > results/2002_MM2_for_Congress.txt
$ scripts/add_list_seats.py 2010 2012 -v > results/2012_MM2_for_Congress.txt

For documentation, type:

$ scripts/add_list_seats.py -h

"""

import argparse
from MM2 import *

parser = argparse.ArgumentParser(
    description="Add MM2 list seats to base congressional apportionment."
)

parser.add_argument("cycle", help="The census cycle (e.g., 2010)", type=int)
parser.add_argument("election", help="The election year (e.g., 2012)", type=int)

parser.add_argument(
    "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
)

args = parser.parse_args()


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
app.eliminate_gap()
