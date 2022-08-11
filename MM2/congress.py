#!/usr/bin/env python3
#
# MM2 for Congress
#

from .apportion import HH_Apportioner
from .analytics import *
from .settings import *


class MM2_Apportioner:
    def __init__(self, census, elections, verbose=False):
        self._base_app = HH_Apportioner(census)
        self._base_app.assign_N(435)

        # Index the election results by state, and calculate the national results.

        indexed_elections = {}
        totals = {"REP_V": 0, "DEM_V": 0, "REP_S": 0, "DEM_S": 0, "OTH_S": 0}

        for state in elections:
            fV = state["DEM_V"] / (state["REP_V"] + state["DEM_V"])
            nS = state["DEM_S"]
            indexed_elections[state["XX"]] = {"fV": fV, "nS": nS}

            totals["REP_V"] += state["REP_V"]
            totals["DEM_V"] += state["DEM_V"]
            totals["REP_S"] += state["REP_S"]
            totals["DEM_S"] += state["DEM_S"]
            totals["OTH_S"] += state["OTH_S"]

        self._elections = indexed_elections

        self.fV = totals["DEM_V"] / (totals["REP_V"] + totals["DEM_V"])
        # self.fS = totals["DEM_S"] / (totals["REP_S"] + totals["DEM_S"])
        self.nPR = pr_seats(totals["REP_S"] + totals["DEM_S"], self.fV)
        self.nGap = ue_seats(self.nPR, totals["DEM_S"])

        self.list_seats = {}
        template = {"REP": 0, "DEM": 0}
        for xx in STATES:
            self.list_seats[xx] = template.copy()

        self._verbose = verbose


### HELPERS ###


def pick_party(fV, fS):
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

    party = Party.REP if (fS > fV) else Party.DEM

    return party
