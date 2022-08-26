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
        self._base_app.assign_first_N(435)

        # Index the election results by state, and calculate the national results.

        indexed_elections = {}
        totals = {"REP_V": 0, "DEM_V": 0, "REP_S": 0, "DEM_S": 0, "OTH_S": 0}

        for state in elections:
            v_i = state["DEM_V"]
            t_i = state["REP_V"] + state["DEM_V"]
            s_i = state["DEM_S"]
            n_i = (
                state["REP_S"] + state["DEM_S"] + state["OTH_S"]
            )  # The apportioned # of seats

            indexed_elections[state["XX"]] = {
                "v_i": v_i,
                "t_i": t_i,
                "s_i": s_i,
                "n_i": n_i,
            }

            totals["REP_V"] += state["REP_V"]
            totals["DEM_V"] += state["DEM_V"]
            totals["REP_S"] += state["REP_S"]
            totals["DEM_S"] += state["DEM_S"]
            totals["OTH_S"] += state["OTH_S"]

        self._elections = indexed_elections

        # These are fixed - national D vote and two-party vote totals
        self.V = totals["DEM_V"]
        self.T = totals["REP_V"] + totals["DEM_V"]  # NOTE: Removes "other" seats.

        # These grow; snapshot initial values - national D seats and two-party seats
        self.S = totals["DEM_S"]
        self.N = totals["REP_S"] + totals["DEM_S"]  # NOTE: Removes "other" seats.

        self.S0 = self.S
        self.N0 = self.N

        # This changes - the delta from PR
        self.gap = gap_seats(self.V, self.T, self.S, self.N)

        # Initialize the list pool on a copy of the base apportionment by state

        self.reps = {}
        for xx in STATES:
            self.reps[xx] = {}
            self.reps[xx]["ANY"] = self._base_app.reps[xx]

        for xx in STATES:
            self.reps[xx]["REP"] = 0
            self.reps[xx]["DEM"] = 0

        # Initialize the assignment log

        self.log = []

        self._verbose = verbose

    def assign_next(self, strategy):
        # Assign the next seat to the state with the highest priority value.

        hs, pv, xx, _ = self._base_app.assign_next()

        # Gather relevant data for the assignment log.

        v_i = self._elections[xx]["v_i"]
        t_i = self._elections[xx]["t_i"]
        s_i = self._elections[xx]["s_i"] + self.reps[xx]["DEM"]
        n_i = self.reps[xx]["ANY"] + self.reps[xx]["REP"] + self.reps[xx]["DEM"]

        Vf = v_i / t_i
        Sf = s_i / n_i
        d_skew = skew_pct(v_i, t_i, s_i + 1, n_i + 1)
        r_skew = skew_pct(v_i, t_i, s_i, n_i + 1)
        threshold = skew_threshold(0.1, n_i)
        gap = self.gap

        # Assign it to a party using the designated strategy

        match strategy:
            case 0:
                party = minimize_state_skew_retro(Vf, Sf)
            case 1:
                party = minimize_state_skew(d_skew, r_skew)
            # TODO - add more strategies
            case _:
                raise ValueError("Invalid strategy")

        self.reps[xx][party] += 1

        # Housekeeping

        self.N += 1
        if party == "DEM":
            self.S += 1

        ss = self.reps[xx]["ANY"] + self.reps[xx]["REP"] + self.reps[xx]["DEM"]

        return (hs, pv, xx, ss, party, Vf, Sf, d_skew, r_skew, threshold)

    def eliminate_gap(self, strategy=1):
        # Report the PR gap to be closed

        self.baseline = "D's got {:.2%} of the vote and won {:3} of {:3} seats yielding a gap of {:+2} seats.".format(
            self.V / self.T, self.S, self.N, self.gap
        )

        while self.gap > 0:
            # Assign a list seat

            (
                hs,
                pv,
                xx,
                ss,
                party,
                Vf,
                Sf,
                d_skew,
                r_skew,
                threshold,
            ) = self.assign_next(strategy)

            # Recompute the gap

            self.gap = gap_seats(self.V, self.T, self.S, self.N)

            # Log the assignment

            self.log.append(
                {
                    "HOUSE SEAT": hs,
                    "PRIORITY VALUE": pv,
                    "STATE": xx,
                    "STATE SEAT": ss,
                    "Vf": Vf,
                    "Sf": Sf,
                    "SKEW|D": d_skew,
                    "SKEW|R": r_skew,
                    "THRESHOLD": threshold,
                    "PARTY": party,
                    "GAP": self.gap,
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
            v_i = self._elections[xx]["v_i"]
            t_i = self._elections[xx]["t_i"]
            s_i = self._elections[xx]["s_i"] + self.reps[xx]["DEM"]
            n_i = self.reps[xx]["ANY"] + self.reps[xx]["REP"] + self.reps[xx]["DEM"]

            if (((s_i / n_i) - (v_i / t_i)) * n_i) > 1:
                unbalanced.append(xx)

        return unbalanced


### HELPERS ###


# TODO - Add tests
def gap_seats(V, T, S, N):
    PR = pr_seats(N, V / T)
    gap = ue_seats(PR, S)

    return gap


# TODO - Add tests
def skew_pct(V, T, S, N):
    skew = abs(disproportionality(pr_seats(N, V / T) / N, S / N))

    return skew


# TODO - Add tests
def minimize_state_skew(d_skew, r_skew):
    """
    Pick the party that minimizes *prospective* skew.
    """

    party = "REP" if r_skew < d_skew else "DEM"

    return party


# TODO - How/where does this yield different results than minimize_state_skew?!?
def minimize_state_skew_retro(Vf, Sf):
    """
    Pick the party that results in the *least* disproportionality (retrospective).
    """

    party = "REP" if Sf > Vf else "DEM"

    return party


# TODO - Add tests
def skew_threshold(pct, N):
    """
    A state skew (disproportionality) threshold that is 'good enough'
    after which point the national gap can be reduced instead.
    """

    return max(pct, 1 / N)
