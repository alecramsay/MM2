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


def reps_for_control(assembly_size):
    """
    The number of seats needed to control an assembly.
    reps_for_control(435) => 218
    reps_for_control(600) => 301
    """
    n = round((assembly_size / 2) + EPSILON)
    if assembly_size % 2 == 0:
        n += 1

    return n


def slack_formula(D, N):
    """
    The # of seats of slack for the majority vote-winning party (+:R, -:D).
    * D is the # of seats expected for D's.
    * N is the total # of seats.
    * C is the # of seats needed to control the assembly.
    """
    C = reps_for_control(N)

    return (-1 * (D - C)) if (D >= C) else (N - D - C)
