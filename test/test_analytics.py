#!/usr/bin/env python3
#
# TEST ANALYTICS
#

from MM2 import *


class TestAnalytics:
    def test_pr_seats(self):
        N = 10

        Vf = 0.4
        PR = pr_seats(N, Vf)
        assert PR == 4

        Vf = 0.5
        PR = pr_seats(N, Vf)
        assert PR == 5

        Vf = 0.6
        PR = pr_seats(N, Vf)
        assert PR == 6

        Vf = 0.51
        PR = pr_seats(N, Vf)
        assert PR == 5

        Vf = 0.56
        PR = pr_seats(N, Vf)
        assert PR == 6

    def test_ue_seats(self):
        PR = 5

        S = 3
        ue = ue_seats(PR, S)
        assert ue == 2

        S = 4
        ue = ue_seats(PR, S)
        assert ue == 1

        S = 5
        ue = ue_seats(PR, S)
        assert ue == 0

        S = 6
        ue = ue_seats(PR, S)
        assert ue == -1

        S = 7
        ue = ue_seats(PR, S)
        assert ue == -2
