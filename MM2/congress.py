#!/usr/bin/env python3
#
# MM2 for Congress
#

from .apportion import HH_Apportioner
from .analytics import *
from .settings import *


class MM2_Apportioner:
    def __init__(self, census, elections, verbose=False):
        # Apportion the first 435 seats, using Census data.

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
        self.nNominalSeats = (
            totals["REP_S"] + totals["DEM_S"]
        )  # NOTE: Removes "other" seats.
        self.nPR = pr_seats(self.nNominalSeats, self.fV)
        self.nDemSeats = totals["DEM_S"]
        self.nGap = ue_seats(self.nPR, self.nDemSeats)

        # Initialize the list pool on a copy of the base apportionment by state

        self.reps = {}
        for xx in STATES:
            self.reps[xx] = {}
            self.reps[xx]["ANY"] = self._base_app.reps[xx]

        self.nListSeats = 0
        self.nDemListSeats = 0

        for xx in STATES:
            self.reps[xx]["REP"] = 0
            self.reps[xx]["DEM"] = 0

        # Initialize the assignment log

        self.log = []

        self._verbose = verbose

    def eliminate_gap(self):
        # Report the PR gap to be closed

        if self._verbose:
            print(
                "\nD's got {:.2%} of the vote and won {:3} of {:3} seats yielding a gap of {:+2} seats.\n".format(
                    self.fV, self.nDemSeats, self.nNominalSeats, self.nGap
                )
            )

        while self.nGap > 0:
            # Assign a list seat

            hs, pv, xx, ss, party = self.assign_next()

            # Recompute the gap

            N = self.nNominalSeats + self.nListSeats
            D = self.nDemSeats + self.nDemListSeats
            self.nPR = pr_seats(N, self.fV)
            self.nGap = ue_seats(self.nPR, D)

            # Log the assignment

            self.log.append(
                {
                    "HOUSE SEAT": hs,
                    "PRIORITY VALUE": pv,
                    "STATE": xx,
                    "STATE SEAT": ss,
                    "PARTY": party,
                    "GAP": self.nGap,
                }
            )

    def assign_next(self):
        # Assign the next seat to the state with the highest priority value.

        hs, pv, xx, _ = self._base_app.assign_next(list_seat=True)

        # Assign it to the party that makes the state *least* disproportional.

        fV = self._elections[xx]["fV"]
        N = self.reps[xx]["ANY"] + self.reps[xx]["REP"] + self.reps[xx]["DEM"]
        D = self._elections[xx]["nS"] + self.reps[xx]["DEM"]
        fS = D / N

        party = pick_party(fV, fS)
        self.reps[xx][party] += 1

        # Housekeeping

        self.nListSeats += 1
        if party == "DEM":
            self.nDemListSeats += 1
        ss = self.reps[xx]["ANY"] + self.reps[xx]["REP"] + self.reps[xx]["DEM"]

        return (hs, pv, xx, ss, party)


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

    party = "REP" if (fS > fV) else "DEM"

    return party
