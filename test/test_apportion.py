#!/usr/bin/env python3
#
# TEST APPORTIONMENT
#

from MM2 import *


class TestApportioner:
    def test__priority_value(self):

        app = Apportioner(None, None)

        assert app._priority_value(4802982, 2) == 3396221
        assert app._priority_value(4802982, 3) == 1960809

    def test_foo(self):
        csv_data = "data/census/Reapportionment for {} Census.csv".format(2010)
        types = [str, str, int]
        reps_list = read_typed_csv(csv_data, types)

        # TODO

        assert True
