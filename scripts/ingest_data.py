#!/usr/bin/env python3
#

"""
Ingest Chris Warshaw's election data 
"""

from typing import Dict, List

from MM2 import *


### SETUP ###

rawdata: str = "data/census/intake/congress_elections_imputations_2023.csv"
years: List[int] = list(range(1972, 2022 + 1, 2))
csv_dir: str = "data/census/"


def main() -> None:

    print("Do something!")  # TODO

    # Initialize accumulators for a state - a dict
    # Initialize accumulators for all states - a dict of dicts
    # Initialize accumulators for all elections - a dict of dicts of dicts (1972 - 2022)

    # Read the CSV and accumulate the data by state and election (year)

    # Convert the accumulated data to a list of list of dicts -- a list of elections,
    #   where each election is a list of dicts for each state.

    elections: list = list()
    for year in years:
        election: list = list()

        print(f"Flatten the dict of dicts into a list of dicts for {year}")

    # Write each election to a CSV

    for i, year in enumerate(years):
        print(f"Write {year} to CSV")

    pass


if __name__ == "__main__":
    main()

### END ###
