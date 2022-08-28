#!/usr/bin/env python3
#
# TEST MM2 FOR CONGRESS
#

from pytest import approx

from MM2 import *


class TestCongress:
    def test_minimize_state_skew_retro(self):
        # NC : Case 1
        election = {
            "XX": "NC",
            "REP_V": 2137167,
            "DEM_V": 2218357,
            "REP_S": 9,
            "DEM_S": 4,
            "OTH_S": 0,
        }
        v_i = election["DEM_V"]
        t_i = election["REP_V"] + election["DEM_V"]
        s_i = election["DEM_S"]
        n_i = election["REP_S"] + election["DEM_S"]
        party = minimize_state_skew_retro(v_i / t_i, s_i / n_i)

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

    def test_skew_pct(self):
        assert skew_pct(0.5, 1.0, 0.5, 1.0) == approx(0.0)
        assert skew_pct(0.65, 1.0, 0.55, 1.0) == approx(0.1)
        assert skew_pct(0.55, 1.0, 0.65, 1.0) == approx(0.1)
        assert skew_pct(0.53, 1.0, 0.55, 1.0) == approx(0.02)

        # When 'r' = 2
        assert skew_pct(0.5, 1.0, 0.5, 1.0, r=2) == approx(0.0)
        assert skew_pct(0.55, 1.0, 0.60, 1.0, r=2) == approx(0.0)
        assert skew_pct(0.55, 1.0, 0.65, 1.0, r=2) == approx(0.05)
        assert skew_pct(0.45, 1.0, 0.40, 1.0, r=2) == approx(0.0)

    def test_lt_threshold(self):
        assert lt_threshold(0.65 - 0.55, 0.1) == False
        assert lt_threshold(0.55 - 0.65, 0.1) == False
        assert lt_threshold(0.65 - 0.57, 0.1) == True
        assert lt_threshold(0.57 - 0.65, 0.1) == True
