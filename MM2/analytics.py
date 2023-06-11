#!/usr/bin/env python3

"""
PARTISAN ANALYTICS
"""

from pytest import approx

from .constants import *


def pr_seats(N, Vf) -> int:
    """
    The # of seats closest to proportional for a given vote fraction (Vf)
    and number of seats (N).
    """
    PR: int = round((Vf * N) - EPSILON)

    return PR


def ue_seats(PR: int, S: int) -> int:
    """
    Calculate the *whole* # of unearned seats (UE) for a # of D seats.
    Positive values show UE R seats, negative UE D seats.
    """

    UE: int = PR - S

    return UE


def gap_seats(V: int, T: int, S: int, N: int) -> int:
    """
    The *whole* # of seats different from proportional.
    Positive values indicate excess R seats, negative execess D seats.
    """
    PR: int = pr_seats(N, V / T)
    gap: int = ue_seats(PR, S)

    return gap


def disproportionality(Vf: float, Sf: float) -> float:
    """
    Calculate the *fractional* # of disproportional seats for a two-party D seat share (Sf).
    Positive values show disportionality favoring R's', negative values favoring D's.
    """

    return Vf - Sf


def reps_for_control(assembly_size: int) -> int:
    """
    The number of seats needed to control an assembly.
    reps_for_control(435) => 218
    reps_for_control(600) => 301
    """
    n: int = round((assembly_size / 2) + EPSILON)
    if assembly_size % 2 == 0:
        n += 1

    return n


def slack_formula(D: int, N: int) -> int:
    """
    The # of seats of slack for the majority vote-winning party (+:R, -:D).
    * D is the # of seats expected for D's.
    * N is the total # of seats.
    * C is the # of seats needed to control the assembly.
    """
    C: int = reps_for_control(N)

    return (-1 * (D - C)) if (D >= C) else (N - D - C)


def skew_pct(V: int, T: int, S: int, N: int, r: int = 1) -> float | None:
    """
    This is a generalized definition of skew, using an ideal responsiveness, 'r'.
    It expresses the absolute % deviation of the actual seat share from the ideal seat share,
    given 'r'. The simple version where r=1 captures deviation from proportionality.
    When r=2, skew measures the efficiency gap (EG).
    """
    if N < 1:  # No two-party seats
        return None
    if T == 0:  # No two-party votes
        return None

    Vf: float = V / T
    Sf: float = S / N

    skew: float = abs((r * (Vf - 0.5)) - (Sf - 0.5))

    return skew


def skew_threshold(pct: float, N: int) -> float:
    """
    A state skew (disproportionality) threshold that is 'good enough'
    after which point the national gap can be reduced instead.
    """

    return max(pct, 1 / N)


def lt_threshold(x, threshold) -> bool:
    """
    (x < threshold) handling floating point imprecision
    """
    return (abs(x) < threshold) and not abs(x) == approx(threshold)


def expected_slack(V: int, T: int, S: int, N: int) -> int:
    """
    The # of seats of *expected* slack for the majority vote-winning party (+:R, -:D).
    """
    D: int = pr_seats(N, V / T)

    return slack_formula(D, N)


def actual_slack(V: int, T: int, S: int, N: int) -> int:
    """
    The # of seats of *actual* slack for the majority seat-winning party (+:R, -:D).
    """

    return slack_formula(S, N)


### END ###
