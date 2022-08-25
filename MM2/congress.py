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
            Vf = state["DEM_V"] / (state["REP_V"] + state["DEM_V"])
            S = state["DEM_S"]
            indexed_elections[state["XX"]] = {"Vf": Vf, "S": S}

            totals["REP_V"] += state["REP_V"]
            totals["DEM_V"] += state["DEM_V"]
            totals["REP_S"] += state["REP_S"]
            totals["DEM_S"] += state["DEM_S"]
            totals["OTH_S"] += state["OTH_S"]

        self._elections = indexed_elections

        # These are fixed
        self.V = totals["DEM_V"]
        self.T = totals["REP_V"] + totals["DEM_V"]
        self.Vf = self.V / self.T

        self.Reps = totals["REP_S"] + totals["DEM_S"]  # NOTE: Removes "other" seats.

        # These grow
        self.S = totals["DEM_S"]
        self.N = self.Reps

        # This changes
        self.gap = gap_seats(self.N, self.S, self.Vf)
        # TODO - DELETE
        # self.PR = pr_seats(self.Reps, self.Vf)
        # self.nGap = ue_seats(self.PR, self.S)

        # Initialize the list pool on a copy of the base apportionment by state

        self.reps = {}
        for xx in STATES:
            self.reps[xx] = {}
            self.reps[xx]["ANY"] = self._base_app.reps[xx]

        # TODO - DELETE
        # self.L = 0
        # self.nDemListSeats = 0

        for xx in STATES:
            self.reps[xx]["REP"] = 0
            self.reps[xx]["DEM"] = 0

        # Initialize the assignment log

        self.log = []

        self._verbose = verbose

    # TODO - HERE
    def assign_next(self, strategy):
        # Assign the next seat to the state with the highest priority value.

        hs, pv, xx, _ = self._base_app.assign_next()

        # Assign it to the party that makes the state *least* disproportional.

        Vf = self._elections[xx]["Vf"]
        N = self.reps[xx]["ANY"] + self.reps[xx]["REP"] + self.reps[xx]["DEM"]
        D = self._elections[xx]["nS"] + self.reps[xx]["DEM"]
        fS = D / N

        # TODO - Use strategy here
        party = pick_party(Vf, fS)
        self.reps[xx][party] += 1

        # Housekeeping

        self.L += 1
        if party == "DEM":
            self.nDemListSeats += 1
        ss = self.reps[xx]["ANY"] + self.reps[xx]["REP"] + self.reps[xx]["DEM"]

        return (hs, pv, xx, ss, party)

    def eliminate_gap(self, strategy=1):
        # Report the PR gap to be closed

        self.baseline = "D's got {:.2%} of the vote and won {:3} of {:3} seats yielding a gap of {:+2} seats.".format(
            self.Vf, self.nDemSeats, self.Reps, self.nGap
        )

        while self.nGap > 0:
            # Assign a list seat

            hs, pv, xx, ss, party = self.assign_next(strategy)

            # Recompute the gap

            N = self.Reps + self.L
            S = self.nDemSeats + self.nDemListSeats

            self.gap = gap_seats(N, self.S, self.Vf)
            # TODO - DELETE
            # self.PR = pr_seats(N, self.Vf)
            # self.nGap = ue_seats(self.PR, S)

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

    def queue_is_ok(self):
        """
        All states still have priority values in the queue.
        """
        return self._base_app.queue_is_ok()

    def one_rep_states(self):
        """
        Return a list of states with one representative.
        """

        ones = []

        for xx in STATES:
            N = self.reps[xx]["ANY"] + self.reps[xx]["REP"] + self.reps[xx]["DEM"]
            if N == 1:
                ones.append(xx)

        return ones

    def unbalanced_states(self):
        """
        Return a list of states where (Sf - Vf) * N > 1 seat.
        """

        unbalanced = []

        for xx in STATES:
            N = self.reps[xx]["ANY"] + self.reps[xx]["REP"] + self.reps[xx]["DEM"]
            D = self._elections[xx]["nS"] + self.reps[xx]["DEM"]
            fS = D / N
            Vf = self._elections[xx]["Vf"]
            if ((fS - Vf) * N) > 1:
                unbalanced.append(xx)

        return unbalanced


### HELPERS ###


# TODO - Add tests
def gap_seats(N, S, Vf):
    PR = pr_seats(N, Vf)
    gap = ue_seats(PR, S)

    return gap


# TODO - Add tests
def skew_pct(V, T, S, N):
    skew = abs(disproportionality(pr_seats(N, V / T) / N, S / N))

    return skew


def pick_party(Vf, fS):
    """
    Strategies:
    1. Minimize the prospective state skew.
    2. Minimize the prospective national gap.
    3. Balance the two.

    """

    party = "REP" if (fS > Vf) else "DEM"

    return party
