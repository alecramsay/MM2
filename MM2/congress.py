#!/usr/bin/env python3
#
# MM2 for Congress
#


from pytest import approx
from typing import Literal, Callable, Tuple

from .apportion import HH_Apportioner
from .analytics import *
from .settings import *


class MM2_Apportioner:
    def __init__(self, census, elections, min_seats: int = 1, verbose=False) -> None:
        self._census = census
        self._elections = elections
        self._min_seats: int = min_seats
        self._verbose: bool = verbose

        # Apportion the first 435 seats, using census data

        self._base_app: HH_Apportioner = HH_Apportioner(
            census, min_seats=self._min_seats, verbose=verbose
        )
        self._base_app.assign_first_N(NOMINAL_SEATS)

        # Initialize MM2 report structures

        self.byPriority: list = list()
        self.byState: dict = dict()

        # Consolidate census & election data by state

        self._abstract_byState_data()

        # Aggregate national election totals

        self._sum_national_totals()

    def _sum_national_totals(self) -> None:
        totals: dict[str, int] = {
            "REP_V": 0,
            "DEM_V": 0,
            "REP_S": 0,
            "DEM_S": 0,
            "OTH_S": 0,
        }

        for state in self._elections:
            totals["REP_V"] += state["REP_V"]
            totals["DEM_V"] += state["DEM_V"]
            totals["REP_S"] += state["REP_S"]
            totals["DEM_S"] += state["DEM_S"]
            totals["OTH_S"] += state["OTH_S"]

        # - The D vote and two-party vote totals (these are fixed)
        self.V: int = totals["DEM_V"]
        self.T: int = totals["REP_V"] + totals["DEM_V"]  # NOTE: Removes "other" votes.

        # - The D seats and two-party seats (these grow w/ list seats)
        self.S: int = totals["DEM_S"]
        self.N: int = totals["REP_S"] + totals["DEM_S"]  # NOTE: Removes "other" seats.

        # - The initial values for nominal seats
        self.S0: int = self.S
        self.N0: int = self.N

        # - The initial gap & slack (these change)
        self.gap: int = gap_seats(self.V, self.T, self.S, self.N)
        self.slack: int = actual_slack(self.V, self.T, self.S, self.N)

        # Characterize the base apportionment
        self.baseline: str = "D's got {:.2%} of the vote and won {:3} of {:3} seats yielding a gap & slack of {:+2} and {:+2} seats, respectively.".format(
            self.V / self.T, self.S, self.N, self.gap, self.slack
        )

    def _abstract_byState_data(self) -> None:
        for xx in STATES:
            self.byState[xx] = {}

        # Include the census population (POP)
        for state in self._census:
            self.byState[state["XX"]]["POP"] = state["Population"]

        # Add select election data
        for state in self._elections:
            xx: str = state["XX"]

            self.byState[xx]["v"] = state["DEM_V"]
            self.byState[xx]["t"] = state["REP_V"] + state["DEM_V"]
            self.byState[xx]["s"] = state["DEM_S"]
            # NOTE - The apportioned # of seats including "other" seats.
            self.byState[xx]["n"] = state["REP_S"] + state["DEM_S"] + state["OTH_S"]

            self.byState[xx]["v/t"] = self.byState[xx]["v"] / self.byState[xx]["t"]

            # Initialize the total # of D seats including list seats (s'),
            # and the total # of seats including list seats (n')
            self.byState[xx]["s'"] = self.byState[xx]["s"]
            self.byState[xx]["n'"] = self.byState[xx]["n"]

    def assignment_rule(self) -> None:
        # Assign the next seat to the *state* with the highest priority value

        hs: int
        pv: int
        xx: str
        foo: int
        hs, pv, xx, foo = self._base_app.assign_next()

        # Assign it to the *party* based on the chosen strategy

        v_i: int = self.byState[xx]["v"]
        t_i: int = self.byState[xx]["t"]
        s_i: int = self.byState[xx]["s'"]
        n_i: int = self.byState[xx]["n'"]

        Vf: float = v_i / t_i
        Sf: float = s_i / n_i
        d_skew: float = skew_pct(v_i, t_i, s_i + 1, n_i + 1, self._r)
        r_skew: float = skew_pct(v_i, t_i, s_i, n_i + 1, self._r)
        threshold: float = skew_threshold(0.1, n_i)
        gap: int = self.gap  # old gap

        match self._strategy:
            case 0:
                party: Literal["REP", "DEM"] = minimize_state_skew_retro(Vf, Sf)
            case 1:
                # Minimize the prospective skew for the state, until gap is zero
                party = minimize_state_skew(d_skew, r_skew)
            case 2:
                # Reduce the national gap, until gap is zero
                party = self._reducer_fn(gap)
            case 3:
                # Balance the two, until gap is zero
                party = self._balancer_fn(d_skew, r_skew, threshold, gap)
            case 4:
                # Balance the two, until gap is zero, except with skew(r=2)
                party = self._balancer_fn(d_skew, r_skew, threshold, gap)
            case 5:
                # Assign 50 list seats (485 total), reducing the national gap
                party = self._reducer_fn(gap)
            case 6:
                # Assign 165 list seats (600 total), balancing the two with skew(r=2),
                # until gap is zero and then just minimize the national gap
                party = self._balancer_fn(
                    d_skew, r_skew, threshold, gap, self._gap_eliminated
                )
            case 7:
                # Assign 165 list seats (600 total), balancing the two with skew(r=1),
                # until gap is zero and then just minimize the national gap
                party = self._balancer_fn(
                    d_skew, r_skew, threshold, gap, self._gap_eliminated
                )
            case 8:
                # Minimize the prospective skew for the state (r=1), until 165 list seats are assigned
                party = minimize_state_skew(d_skew, r_skew)
            case _:
                raise ValueError("Invalid strategy")

        # Update counters

        if party == "DEM":
            self.byState[xx]["s'"] += 1
            self.S += 1

        self.N += 1
        self.byState[xx]["n'"] += 1
        ss: int = self.byState[xx]["n'"]

        # New gap & slack w/o  "other" seats
        self.gap = gap_seats(self.V, self.T, self.S, self.N)
        self.slack = actual_slack(self.V, self.T, self.S, self.N)

        # Gap has been zeroed (might subsequently go + or -)
        self._gap_eliminated: bool = self._gap_eliminated or self.gap == 0

        # Log the assignment for reporting

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
                "SLACK": self.slack,
            }
        )

    def strategy8_assignment_rule(self) -> None:
        """
        Hard-coded strategy 8 assignment rule vs. multi-strategy assignment rule above
        """

        # Assign the next seat to the *state* with the highest priority value

        hs: int
        pv: int
        xx: str
        foo: int
        hs, pv, xx, foo = self._base_app.assign_next()

        # Assign it to the *party* based on the chosen strategy

        v_i: int = self.byState[xx]["v"]
        t_i: int = self.byState[xx]["t"]
        s_i: int = self.byState[xx]["s'"]
        n_i: int = self.byState[xx]["n'"]

        Vf: float = v_i / t_i
        Sf: float = s_i / n_i
        d_skew: float = skew_pct(v_i, t_i, s_i + 1, n_i + 1, self._r)
        r_skew: float = skew_pct(v_i, t_i, s_i, n_i + 1, self._r)
        threshold: float = skew_threshold(0.1, n_i)
        gap: int = self.gap  # old gap

        # Minimize the prospective skew for the state (r=1), until 165 list seats are assigned
        party: Literal["REP", "DEM"] = minimize_state_skew(d_skew, r_skew)

        # Update counters

        if party == "DEM":
            self.byState[xx]["s'"] += 1
            self.S += 1

        self.N += 1
        self.byState[xx]["n'"] += 1
        ss: int = self.byState[xx]["n'"]

        # New gap & slack w/o  "other" seats
        self.gap = gap_seats(self.V, self.T, self.S, self.N)
        self.slack = actual_slack(self.V, self.T, self.S, self.N)

        # Log the assignment for reporting

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
                "SLACK": self.slack,
            }
        )

    def termination_rule(self) -> bool:
        if self._strategy in [1, 2, 3, 4]:
            # Stop when the gap is zero
            return self.gap != 0
        elif self._strategy in [5]:
            # Stop when all list seats are assigned
            return (self.N - self.N0) < LIST_SEATS
        elif self._strategy in [6, 7, 8]:
            # Stop when total seats are assigned (including "other" seats)
            return (self.N - self.N0) < (TOTAL_SEATS - NOMINAL_SEATS)
        else:
            raise ValueError("Invalid strategy")

    def eliminate_gap(self, strategy=1) -> None:
        # Pre-processing
        self._setup_strategy(strategy)

        while self.termination_rule():
            self.assignment_rule()

        # Post-processing for reports
        self._calc_analytics()

    def _setup_strategy(self, strategy) -> None:
        self._strategy: int = strategy
        self._r: int = 2 if strategy in [4, 6] else 1
        self._gap_eliminated = True if self.gap == 0 else False

        self._reducer_fn: Callable[[int], Literal["DEM", "REP"]] = make_reducer_fn(
            self.V, self.T
        )
        self._balancer_fn: Callable[
            [float, float, float, int, bool], Literal["REP", "DEM"]
        ] = make_balancer_fn(self._reducer_fn)

    def _calc_analytics(self) -> None:
        # Compute the SKEW & POWER for the nominal seats
        for k, v in self.byState.items():
            self.byState[k]["SKEW"] = skew_pct(
                v["v"],
                v["t"],
                v["s"],
                v["n"],
                self._r,
            )
            self.byState[k]["POWER"] = v["POP"] / v["n"]

        # Compute the new SKEW & POWER including list seats
        for k, v in self.byState.items():
            self.byState[k]["SKEW'"] = skew_pct(
                v["v"], v["t"], v["s'"], v["n'"], self._r
            )
            self.byState[k]["POWER'"] = v["POP"] / v["n'"]

    def queue_is_ok(self) -> bool:
        """
        All states still have priority values in the queue.
        """
        return self._base_app.queue_is_ok()

    def one_rep_states(self) -> list:
        """
        Return a list of states with one representative.
        """

        ones: list = list()

        for xx in STATES:
            if self.byState[xx]["n'"] == 1:
                ones.append(xx)

        return ones

    def unbalanced_states(self) -> list:
        """
        Return a list of states where (Sf - Vf) * N > 1 seat.
        """

        unbalanced: list = list()

        for xx in STATES:
            v_i: int = self.byState[xx]["v"]
            t_i: int = self.byState[xx]["t"]
            s_i: int = self.byState[xx]["s'"]
            n_i: int = self.byState[xx]["n'"]

            if (((s_i / n_i) - (v_i / t_i)) * n_i) > 1:
                unbalanced.append(xx)

        return unbalanced


### STRATEGIES ###


def minimize_state_skew(d_skew, r_skew) -> Literal["REP", "DEM"]:
    """
    Pick the party that minimizes *prospective* skew.
    """

    party: Literal["REP", "DEM"] = "REP" if r_skew < d_skew else "DEM"

    return party


def minimize_state_skew_retro(Vf, Sf) -> Literal["REP", "DEM"]:
    """
    Pick the party that results in the *least* disproportionality (retrospective).
    """

    party: Literal["REP", "DEM"] = "REP" if Sf > Vf else "DEM"

    return party


def make_reducer_fn(V, T) -> Callable[[int], Literal["DEM", "REP"]]:
    def reduce_national_gap(gap: int) -> Literal["DEM", "REP"]:
        """
        Reduce the national gap by one seat.

        NOTE - The gap can be zero while more list seats are still being assigned.
        At that point, the gap will flip back & forth between +1 and -1.
        """
        if gap > 0:
            return "DEM"
        if gap < 0:
            return "REP"
        # If the gap is zero, assign the seat to the party with the bigger national vote share
        return "DEM" if (V / T) > 0.5 else "REP"

    return reduce_national_gap


def make_balancer_fn(
    reducer_fn,
) -> Callable[[float, float, float, int, bool], Literal["REP", "DEM"]]:
    def balance_state_and_national(
        d_skew, r_skew, threshold, gap, gap_eliminated=False
    ) -> Literal["REP", "DEM"]:
        """
        Balance state skew (pct) and national gap (seats) until the gap has been eliminated.
        Then just minimize the national gap.
        """

        if (
            lt_threshold(d_skew, threshold) and lt_threshold(r_skew, threshold)
        ) or gap_eliminated:
            party: Literal["REP", "DEM"] = reducer_fn(gap)
        else:
            party: Literal["REP", "DEM"] = minimize_state_skew(d_skew, r_skew)

        return party

    return balance_state_and_national


### HELPERS ###


def gap_seats(V, T, S, N) -> int:
    """
    The *whole* # of seats different from proportional.
    Positive values indicate excess R seats, negative execess D seats.
    """
    PR: int = pr_seats(N, V / T)
    gap: int = ue_seats(PR, S)

    return gap


def skew_pct(V: int, T: int, S: int, N: int, r: int = 1) -> float:
    """
    This is a generalized definition of skew, using an ideal responsiveness, 'r'.
    It expresses the absolute % deviation of vote share from the ideal seat share,
    given 'r'. The simple version where r=1 captures deviation from proportionality.
    When r=2, skew measures the efficiency gap (EG).
    """
    Vf: float = V / T
    Sf: float = S / N

    skew: float = abs((r * (Vf - 0.5)) - (Sf - 0.5))

    return skew


def skew_threshold(pct: float, N: int) -> float:
    """
    A state skew (disproportionality) threshold that is 'good enough'
    after which point the national gap can be reduced instead.
    """

    return max(pct, 1 / N)


def lt_threshold(x, threshold) -> bool:
    """
    (x < threshold) handling floating point imprecision
    """
    return (abs(x) < threshold) and not abs(x) == approx(threshold)


def expected_slack(V: int, T: int, S: int, N: int) -> int:
    """
    The # of seats of *expected* slack for the majority vote-winning party (+:R, -:D).
    """
    D: int = pr_seats(N, V / T)

    return slack_formula(D, N)


def actual_slack(V: int, T: int, S: int, N: int) -> int:
    """
    The # of seats of *actual* slack for the majority seat-winning party (+:R, -:D).
    """

    return slack_formula(S, N)
