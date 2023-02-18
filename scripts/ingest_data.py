#!/usr/bin/env python3
#

"""
Ingest Chris Warshaw's election data 
"""

from typing import Dict, List

from MM2 import *


### SETUP ###

rawdata: str = "data/elections/intake/congress_elections_imputations_2023.csv"
years: List[int] = list(range(1972, 2022 + 1, 2))
csv_dir: str = "data/elections"


def main() -> None:
    # Initialize accumulators

    state_bins: dict[str, int] = {
        "REP_V": 0,
        "DEM_V": 0,
        # "OTH_V": 0,
        # "TOT_V": 0,
        "REP_S": 0,
        "DEM_S": 0,
        "OTH_S": 0,
        # "TOT_S": 0,
    }
    election_bins: dict = dict()
    for xx in STATES:
        election_bins[xx] = state_bins.copy()
        election_bins[xx]["STATE"] = STATE_NAMES[xx]
    data_bins: dict = dict()
    for year in years:
        data_bins[year] = election_bins.copy()

    # Read the CSV and accumulate the data by state and election (year)

    field_types: list = [
        int,  # ""
        str,  # "stcd2"
        int,  # "cycle",
        str,  # "stateabrev"
        str,  # "stcd"
        str,  # "dem_share" -- float but contains a few NA's
        float,  # "dem_share_imputed",
        str,  # "dpres" -- float but contains a few NA's
        int,  # "incumb"
        str,  # "winner_dem" -- int but contains a few NA's
        int,  # "uncontested"
        float,  # "votes_dem" -- int but contains a few floats
        float,  # "votes_rep" -- int but contains a few floats
        float,  # "votes_dem_est"
        float,  # "votes_rep_est"
        str,  # "chamber"
    ]
    input: list[dict] = read_typed_csv(rawdata, field_types)

    # Convert the data into the format we want

    subset: list[dict] = list()
    for row in input:
        year: int = row["cycle"]
        xx: str = row["stateabrev"]
        state: str = STATE_NAMES[xx]
        rep_v: int = int(round(row["votes_rep_est"]))
        dem_v: int = int(round(row["votes_dem_est"]))
        rep_s: int = 0
        dem_s: int = 0
        oth_s: int = 0
        if row["winner_dem"] == "NA":
            oth_s = 1
        elif row["winner_dem"] == "1":
            dem_s = 1
        else:
            rep_s = 1

        keep: dict = {
            "YEAR": year,
            "STATE": state,
            "XX": xx,
            "REP_V": rep_v,
            "DEM_V": dem_v,
            "REP_S": rep_s,
            "DEM_S": dem_s,
            "OTH_S": oth_s,
        }
        subset.append(keep)

    # Accumulate the data by state, election (year), and field

    for row in subset:
        year: int = row["YEAR"]
        xx: str = row["XX"]
        for field in state_bins.keys():
            data_bins[year][xx][field] += row[field]

    # Convert the accumulated data to a list of list of dicts -- a list of elections,
    #   where each election is a list of dicts for each state.

    elections: list = list()
    for year in years:
        rows: list = list()
        for key, value in data_bins[year].items():
            row: dict = {"YEAR": year, "XX": key}
            row.update(value)
            rows.append(row)
        elections.append(rows)

    # Write each election to a CSV

    cols: list[str] = [
        "YEAR",
        "STATE",
        "XX",
        "REP_V",
        "DEM_V",
        # "OTH_V",
        # "TOT_V",
        "REP_S",
        "DEM_S",
        "OTH_S",
        # "TOT_S",
        # "VOTE_%",
        # "SEAT_%",
    ]

    for i, year in enumerate(years):
        name: str = f"Congressional Elections ({year}).csv"
        rel_path: str = csv_dir + "/" + name
        rows: list = elections[i]

        write_csv(rel_path, rows, cols)
        continue

    pass


if __name__ == "__main__":
    main()

### END ###
