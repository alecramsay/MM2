#!/usr/bin/env python3
#
# MM2 for Congress
#


from .apportion import HH_Apportioner
from .analytics import *
from .settings import *


class MM2ApportionerBase:
    """Base support for assigning nominal & list seats to seats & parties, used by both the sandbox and final subclasses."""

    def __init__(
        self,
        census: list,
        elections: list,
        list_min: int = 0,
        total_seats: int = 601,
        verbose: bool = False,
    ) -> None:

        # Capture arguments

        self._census: list = census
        self._elections: list = elections
        self._list_min: int = list_min
        self._total_seats: int = total_seats
        self._verbose: bool = verbose

        # Initialize data structures

        self._base_app: HH_Apportioner = HH_Apportioner(census, verbose=verbose)
        self.byPriority: list = list()
        self.byState: dict = dict()
        for xx in STATES:
            self.byState[xx] = {}

        self.summary: dict = dict()

    def apportion_nominal_seats(self, n: int = 435) -> None:
        self._abstract_census_data()
        self._base_app.assign_first_N(n)
        for k, v in self._base_app.reps.items():
            self.byState[k]["n"] = v  # Total nominal seats vs. two-party seats
            self.byState[k]["n'"] = v  # Accumulator for additional list seats

    ### HOUSEKEEPING HELPERS ###

    def _sum_national_totals(self) -> None:
        """Aggregate national election totals"""
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

        # The D vote and two-party vote totals (these are fixed)
        self.V: int = totals["DEM_V"]
        self.T: int = totals["REP_V"] + totals["DEM_V"]  # NOTE: Removes "other" votes.

        """
        NOTE - There's a bit of legacy cruft here, but it's important to keep it.

        N is initialized next for the Sandbox apportioner class. MM2Apportioner resets N to 435,
        after apportioning the nominal seats, i.e., N there is total seats vs. two-party seats here.

        Initializing N this way for for the Sandbox class, because the termination check is a *delta*
        from this initial value.

        The reason to not factor the Sandbox-specific initialization into that class is that the initial 
        gap & slack values below have *implicitly* removed "other" seats (correctly), and they are used in
        the baseline characterization that follows. This routine works for both code paths.It doesn't matter 
        that N is the total nominal seats (as one would expect) outside the Sandbox class.
        """

        # The D seats and two-party seats (these grow w/ list seats)
        self.S: int = totals["DEM_S"]
        self.N: int = totals["REP_S"] + totals["DEM_S"]  # NOTE: Removes "other" seats.

        # The initial values for nominal seats
        self.S0: int = self.S
        self.N0: int = self.N
        self.O0: int = totals["OTH_S"]

        # The initial gap & slack (these change)
        self.gap: int = gap_seats(self.V, self.T, self.S, self.N)
        self.slack: int = actual_slack(self.V, self.T, self.S, self.N)
        self.skew: float = skew_pct(
            self.V, self.T, self.S, self.N
        )  # N is two-party seats here

        # Characterize the base apportionment
        self.baseline: str = "D's got {:.2%} of the vote and won {:3} of {:3} seats yielding a gap (skew) of {:+2} ({:.2%}) seats (%), respectively.".format(
            self.V / self.T, self.S, self.N, self.gap, self.skew
        )
        # self.baseline: str = "D's got {:.2%} of the vote and won {:3} of {:3} seats yielding a gap & slack of {:+2} and {:+2} seats, respectively.".format(
        #     self.V / self.T, self.S, self.N, self.gap, self.slack
        # )

        # Capture summary data
        self.summary["Year"] = self.YYYY

        self.summary["V_D_%"] = self.V / self.T
        self.summary["N_T"] = 435
        self.summary["N_I"] = totals["OTH_S"]
        self.summary["N_R"] = totals["REP_S"]
        self.summary["N_D"] = totals["DEM_S"]
        self.summary["N_D_%"] = totals["DEM_S"] / (totals["REP_S"] + totals["DEM_S"])

        self.summary["L_T"] = self._total_seats - 435
        self.summary["L_I"] = 0

        self.summary["O_T"] = self._total_seats

    def _abstract_census_data(self) -> None:
        """Keep census population by state"""
        for state in self._census:
            self.byState[state["XX"]]["POP"] = state["Population"]

            # NOTE - Add "n" and "n'" accumulator to byState when apportioning seats to states

            continue

    def _abstract_election_data(self) -> None:
        """Keep two-party election data by state"""
        for i, state in enumerate(self._elections):
            if i == 0:
                self.YYYY: int = state["YEAR"]

            xx: str = state["XX"]

            self.byState[xx]["v"] = state["DEM_V"]
            self.byState[xx]["t"] = state["REP_V"] + state["DEM_V"]
            self.byState[xx]["s"] = state["DEM_S"]

            # Track "other" wins, so they can be removed when assigning list seats & calculating skew
            self.byState[xx]["o"] = state["OTH_S"]

            self.byState[xx]["v/t"] = self.byState[xx]["v"] / self.byState[xx]["t"]

    def _calc_power_by_state(self) -> None:
        # Compute the POWER for the nominal seats
        for k, v in self.byState.items():
            self.byState[k]["POWER"] = v["POP"] / v["n"]

        # Compute the new POWER including list seats
        for k, v in self.byState.items():
            self.byState[k]["POWER'"] = v["POP"] / v["n'"]

    def _calc_skew_by_state(self) -> None:
        """Compute the before & after two-party SKEWs"""
        for k, v in self.byState.items():
            self.byState[k]["SKEW"] = skew_pct(
                v["v"],
                v["t"],
                v["s"],
                v["n"] - v["o"],
                self._r,
            )

        for k, v in self.byState.items():
            self.byState[k]["SKEW'"] = skew_pct(
                v["v"], v["t"], v["s'"], v["n'"] - v["o"], self._r
            )

    ### OUTPUT HELPERS ###

    def queue_is_ok(self) -> bool:
        """
        All states still have priority values in the queue.
        """
        return self._base_app.queue_is_ok()

    def one_rep_states(self) -> list:
        """
        Return a list of states with one representative.
        """

        ones = list()

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

    def summarize(self) -> None:
        """Summarize the apportionment & assignment of list seats"""

        self.summary["L_D"] = self.S - self.S0
        self.summary["L_R"] = self.summary["L_T"] - self.summary["L_D"]
        self.summary["L_D_%"] = self.summary["L_D"] / self.summary["L_T"]

        self.summary["O_D"] = self.summary["N_D"] + self.summary["L_D"]
        self.summary["O_I"] = self.summary["N_I"] + self.summary["L_I"]
        self.summary["O_R"] = self.summary["N_R"] + self.summary["L_R"]
        self.summary["O_D_%"] = self.summary["O_D"] / (
            self.summary["O_D"] + self.summary["O_R"]
        )


class MM2Apportioner(MM2ApportionerBase):
    """The proposed MM2 apportionment algorithm for Congress."""

    def __init__(
        self,
        census: list,
        elections: list,
        list_min: int = 0,
        total_seats: int = 600,
        verbose: bool = False,
    ) -> None:

        super().__init__(
            census,
            elections,
            list_min=list_min,
            total_seats=total_seats,
            verbose=verbose,
        )
        self._r: int = 1

    def apportion_and_assign_seats(self) -> None:
        """Apportion seats and assign party mix (requires election data)"""
        self._abstract_election_data()
        self._sum_national_totals()

        self.apportion_seats()
        self.assign_party_mix()
        self.summarize()

    def apportion_seats(self) -> None:
        """Apportion nominal & list seats based on a census"""

        assert self._list_min == 0 or self._list_min == 1

        self.apportion_nominal_seats()
        self.N: int = 435

        # Apportion list seats, keeping track of the states with no list seats

        no_list_seats: set[str] = {xx for xx in STATES}

        # Assign list seats
        while self.N < self._total_seats:
            # Based on priority values
            self.N += 1
            self._assign_priority_seat()

            no_list_seats.discard(self.assigned_to)

            # Until the remaining seats are needed to ensure every state gets at least one list seat
            if self._list_min == 1 and (self._total_seats - self.N) == len(
                no_list_seats
            ):
                break

        # Assign the remaining seats to states with no list seats, if guaranteed
        if self._list_min == 1:
            for xx in no_list_seats:
                self.N += 1
                self._assign_named_seat(xx)

        # Post-process the results for reports
        self._calc_power_by_state()

    def _assign_priority_seat(self) -> None:
        """Assign the next seat to the *state* with the highest priority value"""

        hs: int
        pv: int
        xx: str
        ss: int
        hs, pv, xx, ss = self._base_app.assign_next()

        # self.N += 1  # Do this in the caller for greater transparency
        self.byState[xx]["n'"] += 1
        self.assigned_to: str = xx

    def _assign_named_seat(self, xx: str) -> None:
        """Assign a seat to a specified state"""

        hs: int
        pv: int
        xx: str
        ss: int
        hs, pv, xx, ss = self._base_app.assign_named(xx)

        # self.N += 1  # Do this in the caller for greater transparency
        self.byState[xx]["n'"] += 1
        self.assigned_to: str = xx

    def assign_party_mix(self) -> None:
        """Assign list seats to parties based on election results"""

        for k, v in self.byState.items():
            two_party_seats: int = v["n"] - v["o"]
            list_seats: int = v["n'"] - v["n"]
            assert v["t"] > 0  # There must be *some* D/R votes
            vote_share: float = v["v"] / v["t"]
            D_wins: int = v["s"]

            D_list: int
            R_list: int
            D_list, R_list = party_split(
                two_party_seats, list_seats, vote_share, D_wins
            )

            self.byState[k]["s'"] = D_wins + D_list
            self.S += D_list

        # Post-process the results for reports
        self._calc_skew_by_state()
        self.gap: int = gap_seats(self.V, self.T, self.S, self.N - self.O0)
        self.skew = skew_pct(self.V, self.T, self.S, self.N - self.O0)


### HELPERS ###


def party_split(
    nominal_seats: int, list_seats: int, vote_share: float, D_wins: int
) -> tuple[int, int]:
    """
    The (D, R) split of list seats

    - D's can't get more list seats than apportioned to the state
    - D's can't *lose* seats, i.e., minimum D list seats is 0
    - Other seats are constant, i.e., removed from the nominal seats

    NOTE - Both nominal_seats and vote_share are *two party* values!
    """

    assert list_seats >= 0

    if list_seats == 0:
        return (0, 0)

    PR: int = pr_seats(nominal_seats + list_seats, vote_share)
    gap: int = ue_seats(PR, D_wins)

    D_list: int = min(max(gap, 0), list_seats)
    R_list: int = list_seats - D_list

    return (D_list, R_list)


### END ###
