#!/usr/bin/env python3
#
# Partisan analytics
#

from .settings import *


def pr_seats(N, Vf):
    """
    The # of seats closest to proportional for a given vote fraction (Vf)
    and number of seats (N).
    """
    PR = round((Vf * N) - EPSILON)

    return PR


def ue_seats(PR, S):
    """
    Calculate the *whole* # of unearned seats (UE) for a # of D seats.
    Positive values show UE R seats, negative UE D seats.
    """

    UE = PR - S

    return UE


def disproportionality(Vf, Sf):
    """
    Calculate the *fractional* # of disproportional seats for a two-party D seat share (Sf).
    Positive values show disportionality favoring R's', negative values favoring D's.
    """

    return Vf - Sf
