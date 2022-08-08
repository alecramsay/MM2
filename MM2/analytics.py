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
    pr = round((Vf * N) - EPSILON)

    return pr


def ue_seats(pr, d_s):
    """
    Calculate the # of unearned seats (UE), given a # of D seats.
    Positive values show UE R seats, negative UE D seats.
    """

    ue = pr - d_s

    return ue
