#!/usr/bin/env python3
#

"""
Q. How big does the House have to be for every state to have multiple seats?
A. For the 2020 census, all states have multiple seats after 811 seats.

   After 435 seats, 6 states have multiple seats: {'AK', 'DE', 'SD', 'ND', 'VT', 'WY'}
   After 473 seats, 5 states have multiple seats: {'AK', 'SD', 'ND', 'VT', 'WY'}        <= 'DE'
   After 526 seats, 4 states have multiple seats: {'AK', 'ND', 'VT', 'WY'}              <= 'SD'
   After 601 seats, 3 states have multiple seats: {'AK', 'VT', 'WY'}                    <= 'ND'
   After 641 seats, 2 states have multiple seats: {'VT', 'WY'}                          <= 'AK'
   After 728 seats, 1 states have multiple seats: {'WY'}                                <= 'VT'
   For the 2020 census, all states have multiple seats after 811 seats.                 <= 'WY'

For example:

$ scripts/multiple_seats.py | grep After

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

while single_seats:
    hs: int
    pv: int
    xx: str
    ss: int
    hs, pv, xx, ss = app.assign_next()

    single_seats.discard(xx)

    if app.N < 435:
        continue

    if app.N == 435:
        n_single_seats: int = len(single_seats)
        print(
            "After {} seats, {} states have multiple seats: {}".format(
                app.N, len(single_seats), single_seats
            )
        )
        continue

    if len(single_seats) < n_single_seats:
        n_single_seats = len(single_seats)
        if n_single_seats > 0:
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
