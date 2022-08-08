#!/usr/bin/env python3
#
# MM2 for Congress
#

from .analytics import *

"""
TODO
- Calculate # proportional seats for each state
- Calculate national two-party D vote share
- Calculate national seat gap (+ = R, - = D)

- Assign additional seats to states
- Calculate disproportionality

"""


def national_results(elections_by_state, verbose=False):
    """
    Calculate the national results for a congressional election.
    """

    totals = {"REP_V": 0, "DEM_V": 0, "REP_S": 0, "DEM_S": 0, "OTH_S": 0}
    for state in elections_by_state:
        totals["REP_V"] += state["REP_V"]
        totals["DEM_V"] += state["DEM_V"]
        totals["REP_S"] += state["REP_S"]
        totals["DEM_S"] += state["DEM_S"]
        totals["OTH_S"] += state["OTH_S"]

    # The *national* two-party D vote share & seat share
    Vf = totals["DEM_V"] / (totals["REP_V"] + totals["DEM_V"])
    Sf = totals["DEM_S"] / (totals["REP_S"] + totals["DEM_S"])

    # The proportional number of D seats (ignoring "other" wins)
    PR = pr_seats(totals["REP_S"] + totals["DEM_S"], Vf)

    # The *national* seat gap (+ = R, - = D)
    gap = ue_seats(PR, totals["DEM_S"])

    return (Vf, Sf, PR, gap)


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
