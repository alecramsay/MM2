#!/usr/bin/env python3

"""
FIND REPRESENTATION THRESHOLD

For each state, find the threshold for a 3rd-party to win a seat in state's US House delegation.

The result is:

threshold = 1 / (N + 1)

where N is the number of seats in the state's US House delegation, including both nominal & list seats.
"""

import copy

from MM2 import *


### SAMPLE DATA for CA 2022 ###

N: int = 52

# parties: list = ["D", "R", "O"]
actual_votes: list[dict] = [
    {"PARTY": "D", "VOTES": 6743737},
    {"PARTY": "R", "VOTES": 3859666},
    {"PARTY": "O", "VOTES": 52965},
]

nominal_seats: list[dict] = [
    {"PARTY": "D", "SEATS": 40},
    {"PARTY": "R", "SEATS": 12},
    {"PARTY": "O", "SEATS": 0},
]

L: int = 19
T: int = N + L

pass

### ARGS ###

verbose: bool = False

### MAIN ###


def main() -> None:
    votes: list[dict] = copy.deepcopy(actual_votes)

    app: DHondt_Apportioner = DHondt_Apportioner(T, votes, verbose)
    app.apportion_seats()
    o_seats: int = app.reps["O"]

    if o_seats < 1:
        indexed: dict = {item["PARTY"]: item["VOTES"] for item in actual_votes}
        offsets: dict = {item["PARTY"]: 0 for item in actual_votes}

        d_votes: int = indexed["D"]
        r_votes: int = indexed["R"]
        o_votes: int = indexed["O"]

        while o_seats < 1:
            # Shift votes to "O" uniformly
            offsets["D"] -= 1
            offsets["R"] -= 1
            offsets["O"] += 2

            d_votes: int = indexed["D"] + offsets["D"]
            r_votes: int = indexed["R"] + offsets["R"]
            o_votes: int = indexed["O"] + offsets["O"]

            assert d_votes >= 0
            assert r_votes >= 0
            assert o_votes >= 0

            if verbose:
                print(f"D: {d_votes} | R: {r_votes} | O: {o_votes}")

            votes = [
                {"PARTY": "D", "VOTES": indexed["D"] + offsets["D"]},
                {"PARTY": "R", "VOTES": indexed["R"] + offsets["R"]},
                {"PARTY": "O", "VOTES": indexed["O"] + offsets["O"]},
            ]

            # and re-run the apportionment
            app = DHondt_Apportioner(T, votes, verbose)
            app.apportion_seats()
            o_seats = app.reps["O"]

        t_votes: int = d_votes + r_votes + o_votes
        print(
            f"D: {d_votes / t_votes:.2%} | R: {r_votes / t_votes:.2%} | O: {o_votes / t_votes:.2%}"
        )

        pass

    pass


if __name__ == "__main__":
    main()

### END ###
