#!/usr/bin/env python3
#
# Partisan analytics
#

from .settings import *


def pr_seats(N, fV):
    """
    The # of seats closest to proportional for a given vote fraction (fV)
    and number of seats (N).
    """
    nPR = round((fV * N) - EPSILON)

    return nPR


def ue_seats(nPR, nS):
    """
    Calculate the *whole* # of unearned seats (UE) for a # of D seats.
    Positive values show UE R seats, negative UE D seats.
    """

    nUE = nPR - nS

    return nUE


def disproportionality(fPR, fS):
    """
    Calculate the *fractional* # of disproportional seats for a two-party D seat share (fS).
    Positive values show disportionality favoring R's', negative values favoring D's.
    """

    fD = fPR - fS

    return fD
