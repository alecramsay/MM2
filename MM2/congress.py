#!/usr/bin/env python3
#
# MM2 for Congress
#

from .analytics import *
from .settings import *


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


def assign_seat(election, verbose=False):
    """
    Assign a newly apportioned seat to the list pool to the R's or D's:
    * If two-party D seat share is greater than the two-party D vote share (Sf > Vf),
      then assign the seat to R's.
    * Otherwise (Sf <= Vf) or ((1 - Sf) > (1 - Vf)), then assign the seat to D's.
    * When Sf == Vf, the state is already proportional, so assigning a new seat will make
      it *less* proportional. Assigning these seats to D's helps counter the inherent
      geographic bias that favors R's.

    For each newly assigned seat, there are three cases:
    * Case 1: # disproportional seats > 1 (so new disproportional seats still > 0)
    * Case 2: # disproportional seats between 0.5 and 1 (so new disproportionality is less)
    * Case 3: # disproportional seats less than 0.5 (so new disproportionality is more).

    So, even though the overall party list pool process will eventaually terminate, each
    state step in the process may not be converging.
    """

    Vf = election["DEM_V"] / (election["REP_V"] + election["DEM_V"])
    N = election["REP_S"] + election["DEM_S"]
    Sf = election["DEM_S"] / N
    PR = pr_seats(N, Vf)
    Df = disproportionality(PR / N, Sf)

    scenario = None
    if abs(Df) * N > 1:
        scenario = "Case 1"
    elif abs(Df) * N > 0.5:
        scenario = "Case 2"
    else:
        scenario = "Case 3"

    party = Party.REP if (Sf > Vf) else Party.DEM

    return (party, Vf, Sf, PR, Df, scenario)


### CONGRESSIONAL APPORTIONMENT ###

"""
See "Calculating Apportionment" in:
https://www.census.gov/content/dam/Census/library/publications/2011/dec/c2010br-08.pdf

The algorithm is the Huntington-Hill method:
https://electionscience.org/library/congressional-apportionment-huntington-hill-method/
https://en.wikipedia.org/wiki/Huntington%E2%80%93Hill_method

Some supporting resources:
https://www.census.gov/topics/public-sector/congressional-apportionment/about/computing.html
https://support.ndsnfp.com/portal/en/community/topic/method-of-equal-proportions-from-the-u-s-census
https://www2.census.gov/programs-surveys/decennial/2010/data/apportionment/PriorityValues2010.pdf

There is implementation, but it's embedded in a general package and hard to understand & verify:
https://pypi.org/project/apportionment/
https://github.com/martinlackner/apportionment

"""
