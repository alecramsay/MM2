#!/usr/bin/env python3
#

"""
Q. How big does the House have to be for every state to have multiple seats?
A. For the 2020 census, all states have multiple seats after 811 seats.
   WY is the last state to get a second seat.

For example:

$ scripts/mutiple_seats.py

"""

from MM2 import *


cycle = 2020
# verbose = True


### LOAD THE CENSUS ###

csv_data = "data/census/{}_census.csv".format(cycle)
types = [str, str, int]
census = read_typed_csv(csv_data, types)


### APPORTION NOMINAL SEATS UNTIL EVERY STATE HAS MORE THAN 1 ###

app = HH_Apportioner(census)

for xx in STATES:
    app.reps[xx] = 1
app.N = 50
single_seats = set(STATES)

app._make_priority_queue()

print("HOUSE SEAT,PRIORITY VALUE,STATE ABBREVIATION,STATE SEAT")

while single_seats:
    hs, pv, xx, ss = app.assign_next()
    print("{},{},{},{}".format(hs, pv, xx, ss))

    single_seats.discard(xx)

print(
    "For the {} census, all states have multiple seats after {} seats.".format(
        cycle, app.N
    )
)
