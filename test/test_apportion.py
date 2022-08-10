#!/usr/bin/env python3
#
# TEST APPORTIONMENT
#

from MM2 import *


class TestApportioner:
    def test__priority_value(self):
        # Any census ...
        csv_data = "data/census/{}_census.csv".format(2010)
        types = [str, str, int]
        census = read_typed_csv(csv_data, types)

        app = Apportioner(census)

        assert app._priority_value(4802982, 2) == 3396221
        assert app._priority_value(4802982, 3) == 1960809

    def test_assign_435(self):
        # Replicate 2010 apportionment
        csv_data = "data/census/{}_census.csv".format(2010)
        types = [str, str, int]
        census = read_typed_csv(csv_data, types)

        app = Apportioner(census)
        app.assign_435()

        csv_data = "data/census/Reapportionment for {} Census.csv".format(2010)
        types = [str, str, int]
        reps_list = read_typed_csv(csv_data, types)

        for state in reps_list:
            xx = state["XX"]
            assert app.reps[xx] == state["REPS"]

        # TODO: 2020

        # TODO: 2000

        # TODO: 1990
