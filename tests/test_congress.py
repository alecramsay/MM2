#!/usr/bin/env python3
#
# TEST MM2 FOR CONGRESS
#

from MM2 import *


class TestCongress:
    def test_assign_seat(self):
        # NC : Case 1
        election = {
            "XX": "NC",
            "REP_V": 2137167,
            "DEM_V": 2218357,
            "REP_S": 9,
            "DEM_S": 4,
            "OTH_S": 0,
        }
        party, Vf, Sf, PR, gap, scenario = assign_seat(election)

        assert party == Party.DEM

        # MD : Case 1

        election = {
            "XX": "MD",
            "REP_V": 858406,
            "DEM_V": 1626872,
            "REP_S": 1,
            "DEM_S": 7,
            "OTH_S": 0,
        }
        party, Vf, Sf, PR, gap, scenario = assign_seat(election)

        assert party == Party.REP

        # WA : Case 2

        election = {
            "XX": "WA",
            "REP_V": 1369540,
            "DEM_V": 1636726,
            "REP_S": 4,
            "DEM_S": 6,
            "OTH_S": 0,
        }
        party, Vf, Sf, PR, gap, scenario = assign_seat(election)

        assert party == Party.REP

        # WI : Case 2

        election = {
            "XX": "WI",
            "REP_V": 1401995,
            "DEM_V": 1445015,
            "REP_S": 5,
            "DEM_S": 3,
            "OTH_S": 0,
        }
        party, Vf, Sf, PR, gap, scenario = assign_seat(election)

        assert party == Party.DEM

        # CO : Case 3

        election = {
            "XX": "CO",
            "REP_V": 1194204,
            "DEM_V": 1187745,
            "REP_S": 4,
            "DEM_S": 3,
            "OTH_S": 0,
        }

        party, Vf, Sf, PR, gap, scenario = assign_seat(election)

        assert party == Party.DEM
