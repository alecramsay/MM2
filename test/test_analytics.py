#!/usr/bin/env python3
#
# TEST ANALYTICS
#

from MM2 import *


class TestAnalytics:
    def test_pr_seats(self) -> None:
        N: int = 10

        Vf: float = 0.4
        PR: int = pr_seats(N, Vf)
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

    def test_ue_seats(self) -> None:
        PR: int = 5

        S: int = 3
        ue: int = ue_seats(PR, S)
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

    def test_number_for_control(self) -> None:
        assert reps_for_control(435) == 218
        assert reps_for_control(434) == 218
        assert reps_for_control(433) == 217
        assert reps_for_control(600) == 301

    def test_slack_formula(self) -> None:
        assert slack_formula(215, 435) == 2
        assert slack_formula(216, 435) == 1
        assert slack_formula(217, 435) == 0
        assert slack_formula(218, 435) == 0
        assert slack_formula(219, 435) == -1
        assert slack_formula(220, 435) == -2

    def test_skew_pct(self) -> None:
        assert skew_pct(0.5, 1.0, 0.5, 1.0) == approx(0.0)
        assert skew_pct(0.65, 1.0, 0.55, 1.0) == approx(0.1)
        assert skew_pct(0.55, 1.0, 0.65, 1.0) == approx(0.1)
        assert skew_pct(0.53, 1.0, 0.55, 1.0) == approx(0.02)

        # When 'r' = 2
        assert skew_pct(0.5, 1.0, 0.5, 1.0, r=2) == approx(0.0)
        assert skew_pct(0.55, 1.0, 0.60, 1.0, r=2) == approx(0.0)
        assert skew_pct(0.55, 1.0, 0.65, 1.0, r=2) == approx(0.05)
        assert skew_pct(0.45, 1.0, 0.40, 1.0, r=2) == approx(0.0)

    def test_skew_threshold(self) -> None:
        assert skew_threshold(0.10, 20) == approx(0.10)
        assert skew_threshold(0.10, 5) == approx(0.20)

    def test_lt_threshold(self) -> None:
        assert lt_threshold(0.65 - 0.55, 0.1) == False
        assert lt_threshold(0.55 - 0.65, 0.1) == False
        assert lt_threshold(0.65 - 0.57, 0.1) == True
        assert lt_threshold(0.57 - 0.65, 0.1) == True


### END ###
