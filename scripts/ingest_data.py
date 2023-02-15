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
csv_dir: str = "data/elections/"


def main() -> None:
    # Initialize accumulators

    state_bins: dict[str, int] = {
        "REP_V": 0,
        "DEM_V": 0,
        "OTH_V": 0,
        "TOT_V": 0,
        "REP_S": 0,
        "DEM_S": 0,
        "OTH_S": 0,
        "TOT_S": 0,
    }
    election_bins: dict = dict()
    for xx in STATES:
        election_bins[xx] = state_bins.copy()
        election_bins[xx]["STATE"] = STATE_NAMES[xx]
    data_bins: dict = dict()
    for year in years:
        data_bins[year] = election_bins.copy()

    # Read the CSV and accumulate the data by state and election (year)

    print("TODO - Read the CSV and accumulate the data by state and election (year)")
    # TODO - read_typed_csv(rel_path, field_types)

    # Accumulate the data by state, election (year), and field

    print("TODO - Accumulate the data by state, election (year), and field")

    # Convert the accumulated data to a list of list of dicts -- a list of elections,
    #   where each election is a list of dicts for each state.

    elections: list = list()
    for year in years:
        rows: list = list()
        for key, value in data_bins[year].items():
            row: dict = {"YEAR": year, "XX": key}
            row.update(value)
            # TODO - Calculate VOTE_% and SEAT_% here

            rows.append(row)
        elections.append(rows)

    # Write each election to a CSV

    cols: list[str] = [
        "YEAR",
        "STATE",
        "XX",
        "REP_V",
        "DEM_V",
        "OTH_V",
        "TOT_V",
        "REP_S",
        "DEM_S",
        "OTH_S",
        "TOT_S",
        "VOTE_%",
        "SEAT_%",
    ]

    for i, year in enumerate(years):
        name: str = f"Congressional Elections ({year}).csv"
        rel_path: str = csv_dir + name
        rows: list = elections[i]

        print(f"Write '{name}' to CSV")
        # TODO -  write_csv(rel_path, rows, cols)

    pass


if __name__ == "__main__":
    main()

### END ###
