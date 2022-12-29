#!/usr/bin/env python3
#

"""
Run variations of Strategy 8 against LOCAL election data:
- 'a' = allocate 1 seat per state, and then up to 600
- 'b' = allocate 2 seats per state, and then up to 600
- 'c' = allocate 1 seat per state, and then up to 600, but ensure > 1 seat per state

For example:

$ scripts/MM2_strategy8_LOCAL.py --c 2020 -e 2022 -o a
$ scripts/MM2_strategy8_LOCAL.py --c 2020 -e 2022 -o b
$ scripts/MM2_strategy8_LOCAL.py --c 2020 -e 2022 -o c


For documentation, type:

$ scripts/MM2_strategy8_LOCAL.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace
from typing import Tuple

from MM2 import *


### MODS FOR LOCAL USE ###

census_root: str = "data/census"
elections_root: str = "/Users/alecramsay/Downloads"


### PARSE ARGUMENTS ###


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Analyze # of seats per state for a census."
    )

    parser.add_argument(
        "-c", "--cycle", default=2020, help="The census cycle (e.g., 2020)", type=int
    )
    parser.add_argument(
        "-e",
        "--election",
        default=2022,
        help="The election year (e.g., 2022)",
        type=int,
    )
    parser.add_argument(
        "-o", "--option", default="a", help="The option: a, b, or c}", type=str
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    args: Namespace = parse_args()

    cycle: int = args.cycle
    strategy: int = 8
    option: str = args.option

    ### LOAD THE CENSUS ###

    csv_data: str = "{}/{}_census.csv".format(census_root, cycle)
    types: list = [str, str, int]
    census: list = read_typed_csv(csv_data, types)

    ### LOAD THE ELECTION RESULTS ###

    csv_data: str = "{}/Congressional Elections ({}).csv".format(
        elections_root, args.election
    )
    types = [str] * 3 + [int] * 8 + [float] * 2
    elections: list = read_typed_csv(csv_data, types)

    ### APPORTION SEATS PER STRATEGY 8 VARIATIONS ###

    # Assign the first 435 seats
    # For option 'b', start with 2 seats per state
    min_seats: int = 2 if option == "b" else 1
    app: MM2_Apportioner = MM2_Apportioner(
        census, elections, min_seats=min_seats, verbose=args.verbose
    )
    app._r: int = 1

    # For option 'c', keep track of states with only 1 seat
    if option == "c":
        single_seats: set[str] = set()
        for xx, data in app.byState.items():
            if data["n"] == 1:
                single_seats.add(xx)

    # Assign 436–600 seats
    while app.N < 600:
        app.strategy8_assignment_rule()

        if option == "c":
            xx: str = app.byPriority[-1]["STATE"]
            single_seats.discard(xx)

            if (600 - app.N) == len(single_seats):
                # Assign the remaining seats to states with only 1 seat
                break

    if option == "c":
        # Assign the remaining seats to states with only 1 seat
        for xx in single_seats:
            app.strategy8_final_assignment_rule(xx)

    # Post-process the results for reports
    app._calc_analytics()

    ### WRITE THE RESULTS ###

    reps_by_state: str = "results/{}_reps_by_state({}{}).csv".format(
        args.election, strategy, option
    )

    write_csv(
        reps_by_state,
        [
            {
                "XX": k,
                "n": v["n"],
                "v/t": v["v/t"],
                "s": v["s"],
                "SKEW": v["SKEW"],
                "POWER": v["POWER"],
                "n'": v["n'"],
                "s'": v["s'"],
                "SKEW'": v["SKEW'"],
                "POWER'": v["POWER'"],
            }
            for k, v in app.byState.items()
        ],
        # rows,
        ["XX", "n", "v/t", "s", "SKEW", "POWER", "n'", "s'", "SKEW'", "POWER'"],
    )

    reps_by_priority: str = "results/{}_reps_by_priority({}{}).csv".format(
        args.election, strategy, option
    )
    write_csv(
        reps_by_priority,
        app.byPriority,
        [
            "HOUSE SEAT",
            "PRIORITY VALUE",
            "STATE",
            "STATE SEAT",
            "Vf",
            "Sf",
            "SKEW|D",
            "SKEW|R",
            "THRESHOLD",
            "PARTY",
            "GAP",
            "SLACK",
        ],
    )

    ### REPORT SOME BASIC INFO ###

    report: str = "results/{}_report({}{}).txt".format(args.election, strategy, option)
    with open(report, "w") as f:
        print("{}\n".format(app.baseline), file=f)

        print(
            "{} list seats ({} Democratic) were added for a total of {}.\n".format(
                app.N - app.N0,
                app.S - app.S0,
                app._base_app.N,  # Reports the total seats, including "other."
            ),
            file=f,
        )

        if not app.queue_is_ok():
            print(
                "Warning: One or more states have no remaining priority values! Increase MAX_STATE_SEATS & re-run.\n",
                file=f,
            )
        else:
            print("All states have remaining priority values.\n", file=f)

        ones: list = app.one_rep_states()
        if len(ones) > 0:
            print(
                "Some states still have only one representative: {}\n".format(
                    ", ".join(ones)
                ),
                file=f,
            )
        else:
            print("All states have more than one representative.\n", file=f)

        unbalanced: list = app.unbalanced_states()
        if len(unbalanced) > 0:
            print(
                "Some states are still disproportional more than one seat: {}\n".format(
                    ", ".join(unbalanced)
                ),
                file=f,
            )
        else:
            print("All states are within one seat of proportional.\n", file=f)


if __name__ == "__main__":
    main()

### END ###
