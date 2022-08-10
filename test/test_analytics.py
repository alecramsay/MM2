#!/usr/bin/env python3
#
# TEST ANALYTICS
#

from MM2 import *


class TestAnalytics:
    def test_pr_seats(self):
        N = 10

        fV = 0.4
        nPR = pr_seats(N, fV)
        assert nPR == 4

        fV = 0.5
        nPR = pr_seats(N, fV)
        assert nPR == 5

        fV = 0.6
        nPR = pr_seats(N, fV)
        assert nPR == 6

    def test_ue_seats(self):
        nPR = 5

        nS = 3
        ue = ue_seats(nPR, nS)
        assert ue == 2

        nS = 4
        ue = ue_seats(nPR, nS)
        assert ue == 1

        nS = 5
        ue = ue_seats(nPR, nS)
        assert ue == 0

        nS = 6
        ue = ue_seats(nPR, nS)
        assert ue == -1

        nS = 7
        ue = ue_seats(nPR, nS)
        assert ue == -2
