#!/usr/bin/env python3
#

"""
Q. How big does the House have to be for every state to have multiple seats?
A. For the 2020 census, all states have multiple seats after 811 seats.
   WY is the last state to get a second seat.

   After 435 seats, 6 states have multiple seats: {'ND', 'SD', 'VT', 'AK', 'DE', 'WY'}
   After 500 seats, 5 states have multiple seats: {'ND', 'SD', 'VT', 'AK', 'WY'}
   After 600 seats, 4 states have multiple seats: {'ND', 'VT', 'AK', 'WY'}
   After 700 seats, 2 states have multiple seats: {'VT', 'WY'}
   After 800 seats, 1 states have multiple seats: {'WY'}

For example:

$ scripts/mutiple_seats.py

"""

from typing import Tuple

from MM2 import *


cycle: int = 2020
# verbose = True


### LOAD THE CENSUS ###

csv_data: str = "data/census/{}_census.csv".format(cycle)
types: list = [str, str, int]
census: list = read_typed_csv(csv_data, types)


### APPORTION NOMINAL SEATS UNTIL EVERY STATE HAS MORE THAN 1 ###

app: HH_Apportioner = HH_Apportioner(census)

for xx in STATES:
    app.reps[xx] = 1
app.N = 50
single_seats: set[str] = set(STATES)

app._make_priority_queue()

print()
print("HOUSE SEAT,PRIORITY VALUE,STATE ABBREVIATION,STATE SEAT")

while single_seats:
    # HACK - The types of this returned tuple don't deconstruct properly.
    # hs, pv, xx, ss = self.assign_next()
    t: Tuple[int, int, str, int] = app.assign_next()
    hs: int = t[0]
    pv: int = t[1]
    xx: str = t[2]
    ss: int = t[3]
    print("{},{},{},{}".format(hs, pv, xx, ss))

    single_seats.discard(xx)

    if (app.N == 435) or (app.N % 100 == 0):
        print(
            "After {} seats, {} states have multiple seats: {}".format(
                app.N, len(single_seats), single_seats
            )
        )

print(
    "For the {} census, all states have multiple seats after {} seats.".format(
        cycle, app.N
    )
)
