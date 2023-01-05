#!/usr/bin/env python3
#
# TEST MM2 FOR CONGRESS
#

from pytest import approx

from MM2 import *


class TestCongress:
    def test_minimize_state_skew_retro(self) -> None:
        # NC : Case 1
        election: dict[str, Any] = {
            "XX": "NC",
            "REP_V": 2137167,
            "DEM_V": 2218357,
            "REP_S": 9,
            "DEM_S": 4,
            "OTH_S": 0,
        }
        v_i: int = election["DEM_V"]
        t_i: int = election["REP_V"] + election["DEM_V"]
        s_i: int = election["DEM_S"]
        n_i: int = election["REP_S"] + election["DEM_S"]
        party: Literal["REP", "DEM"] = minimize_state_skew_retro(v_i / t_i, s_i / n_i)

        assert party == "DEM"

        # MD : Case 1

        election = {
            "XX": "MD",
            "REP_V": 858406,
            "DEM_V": 1626872,
            "REP_S": 1,
            "DEM_S": 7,
            "OTH_S": 0,
        }
        v_i = election["DEM_V"]
        t_i = election["REP_V"] + election["DEM_V"]
        s_i = election["DEM_S"]
        n_i = election["REP_S"] + election["DEM_S"]
        party = minimize_state_skew_retro(v_i / t_i, s_i / n_i)

        assert party == "REP"

        # WA : Case 2

        election = {
            "XX": "WA",
            "REP_V": 1369540,
            "DEM_V": 1636726,
            "REP_S": 4,
            "DEM_S": 6,
            "OTH_S": 0,
        }
        v_i = election["DEM_V"]
        t_i = election["REP_V"] + election["DEM_V"]
        s_i = election["DEM_S"]
        n_i = election["REP_S"] + election["DEM_S"]
        party = minimize_state_skew_retro(v_i / t_i, s_i / n_i)

        assert party == "REP"

        # WI : Case 2

        election = {
            "XX": "WI",
            "REP_V": 1401995,
            "DEM_V": 1445015,
            "REP_S": 5,
            "DEM_S": 3,
            "OTH_S": 0,
        }
        v_i = election["DEM_V"]
        t_i = election["REP_V"] + election["DEM_V"]
        s_i = election["DEM_S"]
        n_i = election["REP_S"] + election["DEM_S"]
        party = minimize_state_skew_retro(v_i / t_i, s_i / n_i)

        assert party == "DEM"

        # CO : Case 3

        election = {
            "XX": "CO",
            "REP_V": 1194204,
            "DEM_V": 1187745,
            "REP_S": 4,
            "DEM_S": 3,
            "OTH_S": 0,
        }
        v_i = election["DEM_V"]
        t_i = election["REP_V"] + election["DEM_V"]
        s_i = election["DEM_S"]
        n_i = election["REP_S"] + election["DEM_S"]
        party = minimize_state_skew_retro(v_i / t_i, s_i / n_i)

        assert party == "DEM"

    def test_minimize_state_skew(self) -> None:
        assert minimize_state_skew(0.05, 0.10) == "DEM"
        assert minimize_state_skew(0.10, 0.05) == "REP"
        assert minimize_state_skew(0.05, 0.05) == "DEM"

    def test_reduce_national_gap(self) -> None:
        fn: Callable[[int], Literal["DEM", "REP"]] = make_reducer_fn(0.51, 1.0)
        assert fn(1) == "DEM"
        assert fn(-1) == "REP"
        assert fn(0) == "DEM"
        fn = make_reducer_fn(0.49, 1.0)
        assert fn(0) == "REP"

    def test_balance_state_and_national(self) -> None:
        fn: Callable[
            [float, float, float, int, bool], Literal["REP", "DEM"]
        ] = make_balancer_fn(make_reducer_fn(0.51, 1.0))
        assert fn(0.05, 0.06, 0.10, 10) == "DEM"
        assert fn(0.06, 0.05, 0.10, 10) == "DEM"
        assert fn(0.15, 0.16, 0.10, 10) == "DEM"
        assert fn(0.16, 0.15, 0.10, 10) == "REP"

        assert fn(0.05, 0.06, 0.10, -10) == "REP"
        assert fn(0.06, 0.05, 0.10, -10) == "REP"
        assert fn(0.15, 0.16, 0.10, -10) == "DEM"
        assert fn(0.16, 0.15, 0.10, -10) == "REP"

    def test_party_split(self) -> None:
        assert party_split(8, 2, 0.5000, 0) == (2, 0)
        assert party_split(8, 2, 0.5000, 1) == (2, 0)
        assert party_split(8, 2, 0.5000, 2) == (2, 0)
        assert party_split(8, 2, 0.5000, 3) == (2, 0)
        assert party_split(8, 2, 0.5000, 4) == (1, 1)
        assert party_split(8, 2, 0.5000, 5) == (0, 2)
        assert party_split(8, 2, 0.5000, 6) == (0, 2)
        assert party_split(8, 2, 0.5000, 7) == (0, 2)
        assert party_split(8, 2, 0.5000, 8) == (0, 2)

        # Actual other/independent wins:
        # YEAR,STATE,XX,REP_V,DEM_V,OTH_V,TOT_V,REP_S,DEM_S,OTH_S,TOT_S
        # 2000,Vermont,VT,51977,14918,216471,283366,0,0,1,1
        assert party_split(0, 1, 0.2230, 0) == (0, 1)
        # 2000,Virginia,VA,1295849,1261158,177947,2734954,6,4,1,11
        assert party_split(10, 4, 0.4932, 4) == (3, 1)
        # 2002,Vermont,VT,72813,0,152442,225255,0,0,1,1
        assert party_split(0, 1, 0.0000, 0) == (0, 1)
        # 2004,Vermont,VT,74271,21684,209053,305008,0,0,1,1
        assert party_split(0, 1, 0.2260, 0) == (0, 1)
        # 2018,Michigan,MI,1944807,2222793,95297,4262897,6,7,1,14
        assert party_split(13, 5, 0.5334, 7) == (3, 2)


### END ###
