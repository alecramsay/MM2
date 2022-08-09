#!/usr/bin/env python3
#
# TEST APPORTIONMENT
#

from MM2 import *


class TestApportioner:
    def test_priority_value(self):

        app = Apportioner(None, None)

        assert app.priority_value(4802982, 2) == 3396221
        assert app.priority_value(4802982, 3) == 1960809
