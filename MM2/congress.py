#!/usr/bin/env python3
#
# MM2 for Congress
#

from .apportion import HH_Apportioner
from .analytics import *
from .settings import *


class MM2_Apportioner:
    def __init__(self, census, elections, verbose=False):

        # Apportion the first 435 seats, using Census data

        self._base_app = HH_Apportioner(census)
        self._base_app.assign_first_N(435)

        # Initialize the by-priority assignment log

        self.byPriority = []

        # Initialize the by-state summary.

        self.byState = {}
        for xx in STATES:
            self.byState[xx] = {}

        # Include the census population (POP)
        for state in self._base_app._census:
            self.byState[state["XX"]]["POP"] = state["Population"]

        # Include the # of apportioned seats (ANY)
        for xx in STATES:
            # TODO - "N"
            self.byState[xx]["ANY"] = self._base_app.reps[xx]

        # Include the # of D list seats (S) and total list seats (N)
        for xx in STATES:
            # TODO - "S"
            self.byState[xx]["REP"] = 0
            self.byState[xx]["DEM"] = 0

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

            # Also add select election data to the by-state summary:
            # - The two-party D vote share (V/T)
            self.byState[state["XX"]]["V/T"] = v_i / t_i
            # - The # of nominal D seats won (S)
            self.byState[state["XX"]]["S"] = s_i
            # - The skew for the nominal districts (SKEW)
            self.byState[state["XX"]]["SKEW"] = skew_pct(v_i, t_i, s_i, n_i)
            # - The population / nominal district (POWER)
            self.byState[state["XX"]]["POWER"] = (
                self.byState[state["XX"]]["POP"] / self.byState[xx]["ANY"]
            )

            totals["REP_V"] += state["REP_V"]
            totals["DEM_V"] += state["DEM_V"]
            totals["REP_S"] += state["REP_S"]
            totals["DEM_S"] += state["DEM_S"]
            totals["OTH_S"] += state["OTH_S"]

        # Election data indexed by state (XX)
        self._elections = indexed_elections

        # Calculate the national results
        # - The D vote and two-party vote totals (these are fixed)
        self.V = totals["DEM_V"]
        self.T = totals["REP_V"] + totals["DEM_V"]  # NOTE: Removes "other" seats.

        # - The D seats and two-party seats (these grow w/ list seats)
        self.S = totals["DEM_S"]
        self.N = totals["REP_S"] + totals["DEM_S"]  # NOTE: Removes "other" seats.

        # - The initial values for nominal seats
        self.S0 = self.S
        self.N0 = self.N

        # - The delta from PR (this changes)
        self.gap = gap_seats(self.V, self.T, self.S, self.N)

        self._verbose = verbose

    def assign_next(self, strategy):

        # Assign the next seat to the state with the highest priority value

        hs, pv, xx, _ = self._base_app.assign_next()

        # Gather relevant data for the assignment log

        v_i = self._elections[xx]["v_i"]
        t_i = self._elections[xx]["t_i"]
        s_i = self._elections[xx]["s_i"] + self.byState[xx]["DEM"]
        n_i = (
            self.byState[xx]["ANY"] + self.byState[xx]["REP"] + self.byState[xx]["DEM"]
        )

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
            case 2:
                party = reduce_national_gap(gap)
            case 3:
                party = balance_state_and_national(d_skew, r_skew, threshold, gap)
            case _:
                raise ValueError("Invalid strategy")

        self.byState[xx][party] += 1

        # Housekeeping

        self.N += 1
        if party == "DEM":
            self.S += 1

        ss = self.byState[xx]["ANY"] + self.byState[xx]["REP"] + self.byState[xx]["DEM"]

        return (hs, pv, xx, ss, party, Vf, Sf, d_skew, r_skew, threshold)

    def eliminate_gap(self, strategy=1):
        # Report the PR gap to be closed

        # TODO - Factor this out
        self.baseline = "D's got {:.2%} of the vote and won {:3} of {:3} seats yielding a gap of {:+2} seats.".format(
            self.V / self.T, self.S, self.N, self.gap
        )

        while self.gap > 0:
            # Assign a list seat & log it for reporting

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

            # TODO - Fold this into the assign_next function
            self.byPriority.append(
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

            # Recompute the gap

            self.gap = gap_seats(self.V, self.T, self.S, self.N)

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
            N = (
                self.byState[xx]["ANY"]
                + self.byState[xx]["REP"]
                + self.byState[xx]["DEM"]
            )
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
            s_i = self._elections[xx]["s_i"] + self.byState[xx]["DEM"]
            n_i = (
                self.byState[xx]["ANY"]
                + self.byState[xx]["REP"]
                + self.byState[xx]["DEM"]
            )

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
def reduce_national_gap(gap):
    """
    Reduce the national gap by one seat.
    """

    party = "DEM" if gap > 0 else "REP"

    return party


# TODO - Add tests
def balance_state_and_national(d_skew, r_skew, threshold, gap):
    """
    Balance state skew (pct) and national gap (seats).
    """

    if (d_skew < threshold) and (r_skew < threshold):
        party = reduce_national_gap(gap)
    else:
        party = minimize_state_skew(d_skew, r_skew)

    return party


# TODO - Add tests
def skew_threshold(pct, N):
    """
    A state skew (disproportionality) threshold that is 'good enough'
    after which point the national gap can be reduced instead.
    """

    return max(pct, 1 / N)
