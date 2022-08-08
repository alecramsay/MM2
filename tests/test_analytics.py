#!/usr/bin/env python3
#
# TEST ANALYTICS
#

from MM2 import *


class TestAnalytics:
    def test_pr_seats(self):
        N = 10

        Vf = 0.4
        pr = pr_seats(N, Vf)
        assert pr == 4

        Vf = 0.5
        pr = pr_seats(N, Vf)
        assert pr == 5

        Vf = 0.6
        pr = pr_seats(N, Vf)
        assert pr == 6

    def test_ue_seats(self):
        pr = 5

        d_s = 3
        ue = ue_seats(pr, d_s)
        assert ue == 2

        d_s = 4
        ue = ue_seats(pr, d_s)
        assert ue == 1

        d_s = 5
        ue = ue_seats(pr, d_s)
        assert ue == 0

        d_s = 6
        ue = ue_seats(pr, d_s)
        assert ue == -1

        d_s = 7
        ue = ue_seats(pr, d_s)
        assert ue == -2
