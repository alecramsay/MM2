#!/usr/bin/env python3
#
# TEST APPORTIONMENT
#

import pytest
from MM2 import *


class TestHH_Apportioner:
    def test__priority_value(self) -> None:
        # Any census ...
        csv_data: str = "data/census/{}_census.csv".format(2010)
        types: list = [str, str, int]
        census: list = read_typed_csv(csv_data, types)

        app: HH_Apportioner = HH_Apportioner(census)

        assert app._priority_value(4802982, 2) == 3396221
        assert app._priority_value(4802982, 3) == 1960809

    @pytest.mark.parametrize("cycle", [1990, 2000, 2010, 2020])
    def test_assign_first_N(self, cycle) -> None:
        csv_data: str = "data/census/{}_census.csv".format(cycle)
        types: list = [str, str, int]
        census: list = read_typed_csv(csv_data, types)

        app: HH_Apportioner = HH_Apportioner(census)
        app.assign_first_N(435)

        csv_data = "data/census/Reapportionment for {} Census.csv".format(cycle)
        types = [str, str, int]
        reps_list: list = read_typed_csv(csv_data, types)

        for state in reps_list:
            xx: str = state["XX"]
            assert app.reps[xx] == state["REPS"]


### END ###
