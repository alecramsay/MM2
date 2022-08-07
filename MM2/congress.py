#!/usr/bin/env python3
#
# MM2 for Congress
#

"""
TODO
- Calculate # proportional seats for each state
- Calculate national two-party D vote share
- Calculate national seat gap (+ = R, - = D)

- Assign additional seats to states
- Calculate disproportionality

- Define RDO enum

- Get 2020 re-apportionment
- Get 2000 re-apportionment
"""


def prop_seats(r_v, d_v, tot_s, verbose=False):
    """
    Calculate the # of D seats closest to proportional,
    for a state or nationally.
    """
    pass


def gap(prop_s, d_s, verbose=False):
    """
    Calculate the national seat gap (+ = R, - = D).
    """
    pass


def assign_seat(rdo_votes, rdo_seats, verbose=False):
    """
    Assign a newly apportioned seat to the list pool to the R's or D's:
    * If two-party D seat share is greater than the two-party D vote share (Sf > Vf),
      then assign the seat to R's.
    * Otherwise (Sf <= Vf) or ((1 - Sf) > (1 - Vf)), then assign the seat to D's.

    For each newly assigned seat, there are three cases:
    * Case 1: # disproportional seats > 1 (so new disproportional seats still > 0)
    * Case 2: # disproportional seats between 0.5 and 1 (so new disproportionality is less)
    * Case 3: # disproportional seats less than 0.5 (so new disproportionality is more)

    So, even though the overall party list pool process will eventaually terminate, each
    state step in the process may not be converging.
    """
    pass


print("MM2 for Congress ...")
