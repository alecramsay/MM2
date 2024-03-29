#!/usr/bin/env python3
#
# Sandbox for exploring various strategies for assigning list seats to seats & parties.
#


from pytest import approx
from typing import Literal, Callable

from .congress import *
from .analytics import *
from .constants import *


class MM2ApportionerSandbox(MM2ApportionerBase):
    """A sandbox for exploring various strategies for assigning list seats to seats & parties."""

    def __init__(
        self,
        census: list,
        elections: list,
        verbose: bool,
    ) -> None:

        super().__init__(
            census,
            elections,
            list_min=0,  # Backward compatibility; not used
            total_seats=600,  # Ditto
            verbose=verbose,
        )
        self._abstract_byState_data()
        self._sum_national_totals()
        self._base_app.assign_first_N(435)

    def _abstract_byState_data(self) -> None:
        """Legacy combo"""
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

            # Track "other" wins, so they can be removed when assigning list seats & calculating skew
            self.byState[xx]["o"] = state["OTH_S"]

            self.byState[xx]["v/t"] = self.byState[xx]["v"] / self.byState[xx]["t"]

            # Initialize the total # of D seats including list seats (s'),
            # and the total # of seats including list seats (n')
            self.byState[xx]["s'"] = self.byState[xx]["s"]
            self.byState[xx]["n'"] = self.byState[xx]["n"]

    def _calc_analytics_by_state(self) -> None:
        """Legacy combo"""
        self._calc_power_by_state()
        self._calc_skew_by_state()

    ### Strategy 8 ###

    def strategy8(self, *, size: int = 600, option: str = "a") -> None:
        """
        Strategy 8:
        * Assign the first 435 seats using the current approach
          - Give each state 1 representative,
          - Then assign the remaining seats using the queue of priority values
        * Then assign list seats
        * There are two degress of freedom still:
          - The total size of the House (or the number of list seats), and
          - Whether states are guaranteed at least one list seat ('a' = No, 'e' = Yes).
            To guarantee list seats if necessary, they are assigned with the last
            few seats.

        NOTE - This HACK uses a direct size argument, as opposed to one passed when
        the apportioner is instantiated.
        """

        no_list_seats: set[str] = set()
        # For option 'e', keep track of states with no list seats
        if option == "e":
            # no_list_seats: set[str] = set()
            for xx in STATES:
                no_list_seats.add(xx)

        # Assign 436 to the the total size including list seats, e.g., 600, 650, etc.
        while self.N < size:
            self.strategy8_assignment_rule()

            if option == "e":
                xx: str = self.byPriority[-1]["STATE"]
                no_list_seats.discard(xx)

                # NOTE - This might have a problem with "other" seats
                if (size - self.N) == len(no_list_seats):
                    # Assign the remaining seats to states with no list seats
                    break

        if option == "e":
            # Assign the remaining seats to states with no list seats
            for xx in no_list_seats:
                self.strategy8_final_assignment_rule(xx)

        # Post-process the results for reports
        self._calc_analytics_by_state()

    def strategy8_assignment_rule(self) -> None:
        """
        Hard-coded strategy 8 assignment rule vs. multi-strategy assignment rule below:
        - With each list seat, minimize state skew.
        """

        # Assign the next seat to the *state* with the highest priority value

        hs: int
        pv: int
        xx: str
        ss: int
        hs, pv, xx, ss = self._base_app.assign_next()

        # Assign it to the *party* based on the chosen strategy

        v_i: int = self.byState[xx]["v"]
        t_i: int = self.byState[xx]["t"]
        s_i: int = self.byState[xx]["s'"]
        n_i: int = self.byState[xx]["n'"]

        Vf: float = v_i / t_i
        Sf: float = s_i / n_i
        # NOTE - n_i + 1 is always positive; can't be zero
        d_skew: float | None = skew_pct(v_i, t_i, s_i + 1, n_i + 1, self._r)
        r_skew: float | None = skew_pct(v_i, t_i, s_i, n_i + 1, self._r)
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

        # New gap & slack w/o  "other" seats
        self.gap = gap_seats(self.V, self.T, self.S, self.N)
        self.slack = actual_slack(self.V, self.T, self.S, self.N)
        self.skew: float | None = skew_pct(
            self.V, self.T, self.S, self.N
        )  # N is two-party seats here

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

    def strategy8_final_assignment_rule(self, xx: str) -> None:
        """
        Assign the final list seats to the states that still don't have a list seat,
        i.e., override the precedence of the priority value queue.
        """

        # Explicitly assign a seat to a state

        hs: int
        pv: int
        _: str
        ss: int
        hs, pv, _, ss = self._base_app.assign_named(xx)

        # Assign it to the *party* based on the chosen strategy

        v_i: int = self.byState[xx]["v"]
        t_i: int = self.byState[xx]["t"]
        s_i: int = self.byState[xx]["s'"]
        n_i: int = self.byState[xx]["n'"]

        Vf: float = v_i / t_i
        Sf: float = s_i / n_i
        # NOTE - n_i + 1 is always positive; can't be zero
        d_skew: float | None = skew_pct(v_i, t_i, s_i + 1, n_i + 1, self._r)
        r_skew: float | None = skew_pct(v_i, t_i, s_i, n_i + 1, self._r)
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

        # New gap & slack w/o  "other" seats
        self.gap = gap_seats(self.V, self.T, self.S, self.N)
        self.slack = actual_slack(self.V, self.T, self.S, self.N)
        self.skew: float | None = skew_pct(
            self.V, self.T, self.S, self.N
        )  # N is two-party seats here

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

    ### Machinery to facilitate exploring alternate strategies ###

    def assignment_rule(self) -> None:
        # Assign the next seat to the *state* with the highest priority value

        hs: int
        pv: int
        xx: str
        ss: int
        hs, pv, xx, ss = self._base_app.assign_next()

        # Assign it to the *party* based on the chosen strategy

        v_i: int = self.byState[xx]["v"]
        t_i: int = self.byState[xx]["t"]
        s_i: int = self.byState[xx]["s'"]
        n_i: int = self.byState[xx]["n'"]

        Vf: float = v_i / t_i
        Sf: float = s_i / n_i
        # NOTE - n_i + 1 is always positive; can't be zero
        d_skew: float | None = skew_pct(v_i, t_i, s_i + 1, n_i + 1, self._r)
        r_skew: float | None = skew_pct(v_i, t_i, s_i, n_i + 1, self._r)
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
                party = self._balancer_fn(d_skew, r_skew, threshold, gap, False)
            case 4:
                # Balance the two, until gap is zero, except with skew(r=2)
                party = self._balancer_fn(d_skew, r_skew, threshold, gap, False)
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

        # New gap & slack w/o  "other" seats
        self.gap = gap_seats(self.V, self.T, self.S, self.N)
        self.slack = actual_slack(self.V, self.T, self.S, self.N)
        self.skew = skew_pct(
            self.V, self.T, self.S, self.N
        )  # N is two-party seats here

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

    def termination_rule(self) -> bool:
        if self._strategy in [1, 2, 3, 4]:
            # Stop when the gap is zero
            return self.gap != 0
        elif self._strategy in [5]:
            # Stop when all list seats are assigned
            # The number of list seats, for Strategy 5 is 50.
            LIST_SEATS: int = 50
            return (self.N - self.N0) < LIST_SEATS
        elif self._strategy in [6, 7, 8]:
            # Stop when all list seats are assigned
            return (self.N - self.N0) < (self._total_seats - 435)
        else:
            raise ValueError("Invalid strategy")

    def eliminate_gap(self, strategy=1) -> None:
        # Pre-processing
        self._setup_strategy(strategy)

        while self.termination_rule():
            self.assignment_rule()

        # Post-processing for reports
        self._calc_analytics_by_state()

    def _setup_strategy(self, strategy) -> None:
        self._strategy: int = strategy
        self._r: int = 2 if strategy in [4, 6] else 1
        self._gap_eliminated = True if self.gap == 0 else False

        self._reducer_fn: Callable[[int], Literal["DEM", "REP"]] = make_reducer_fn(
            self.V, self.T
        )
        self._balancer_fn: Callable[
            [float | None, float | None, float, int, bool], Literal["REP", "DEM"]
        ] = make_balancer_fn(self._reducer_fn)


### LIST SEAT ASSIGNMENT STRATEGIES ###


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
) -> Callable[[float | None, float | None, float, int, bool], Literal["REP", "DEM"]]:
    def balance_state_and_national(
        d_skew: float | None,
        r_skew: float | None,
        threshold: float,
        gap: int,
        gap_eliminated=False,
    ) -> Literal["REP", "DEM"]:
        """
        Balance state skew (pct) and national gap (seats) until the gap has been eliminated.
        Then just minimize the national gap.
        """

        if d_skew is None or r_skew is None:
            raise ValueError("d_skew and r_skew must be floats")

        if (
            lt_threshold(d_skew, threshold) and lt_threshold(r_skew, threshold)
        ) or gap_eliminated:
            party: Literal["REP", "DEM"] = reducer_fn(gap)
        else:
            party: Literal["REP", "DEM"] = minimize_state_skew(d_skew, r_skew)

        return party

    return balance_state_and_national


### END ###
