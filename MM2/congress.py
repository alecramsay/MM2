#!/usr/bin/env python3
#
# MM2 for Congress
#

from .analytics import *
from .settings import *


def assign_seat(election, verbose=False):
    """
    Assign a newly apportioned seat to the list pool to the R's or D's:
    * If two-party D seat share is greater than the two-party D vote share (fS > fV),
      then assign the seat to R's.
    * Otherwise (fS <= fV) or ((1 - fS) > (1 - fV)), then assign the seat to D's.
    * When fS == fV, the state is already proportional, so assigning a new seat will make
      it *less* proportional. Assigning these seats to D's helps counter the inherent
      geographic bias that favors R's.

    For each newly assigned seat, there are three cases:
    * Case 1: # disproportional seats > 1 (so new disproportional seats still > 0)
    * Case 2: # disproportional seats between 0.5 and 1 (so new disproportionality is less)
    * Case 3: # disproportional seats less than 0.5 (so new disproportionality is more).

    So, even though the overall party list pool process will eventaually terminate, each
    state step in the process may not be converging.
    """

    fV = election["DEM_V"] / (election["REP_V"] + election["DEM_V"])
    N = election["REP_S"] + election["DEM_S"]
    fS = election["DEM_S"] / N

    party = Party.REP if (fS > fV) else Party.DEM

    return party


### HELPERS ###


def national_results(elections, verbose=False):
    """
    Calculate the national results for a congressional election.
    """

    totals = {"REP_V": 0, "DEM_V": 0, "REP_S": 0, "DEM_S": 0, "OTH_S": 0}
    for state in elections:
        totals["REP_V"] += state["REP_V"]
        totals["DEM_V"] += state["DEM_V"]
        totals["REP_S"] += state["REP_S"]
        totals["DEM_S"] += state["DEM_S"]
        totals["OTH_S"] += state["OTH_S"]

    # The *national* two-party D vote share & seat share
    fV = totals["DEM_V"] / (totals["REP_V"] + totals["DEM_V"])
    fS = totals["DEM_S"] / (totals["REP_S"] + totals["DEM_S"])

    # The proportional number of D seats (ignoring "other" wins)
    nPR = pr_seats(totals["REP_S"] + totals["DEM_S"], fV)

    # The *national* seat gap (+ = R, - = D)
    nGap = ue_seats(nPR, totals["DEM_S"])

    return (fV, nGap)
