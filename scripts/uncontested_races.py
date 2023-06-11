#!/usr/bin/env python3

"""
Report uncontested races by year, state, and district using Chris Warshaw's election data 

For example:

scripts/uncontested_races.py
"""

from typing import List

from MM2 import *


### SETUP ###

rawdata: str = "data/elections/intake/congress_elections_imputations_2023.csv"
years: List[int] = list(range(1972, 2022 + 1, 2))
csv_dir: str = "data/elections"


def main() -> None:
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
    input: list[dict] = read_csv(rawdata, field_types)

    # Find & report uncontested races

    print(f"YEAR,XX, STATE,DISTRICT,UNCONTESTED")
    for row in input:
        if row["uncontested"] == 0:
            continue

        # Uncontested races

        year: int = row["cycle"]
        xx: str = row["stateabrev"]
        state: str = STATE_NAMES[xx]
        district: int = (
            int(row["stcd"][1:]) if len(row["stcd"]) == 3 else int(row["stcd"][2:])
        )

        uncontested: str
        if row["winner_dem"] == "NA":
            uncontested = "Other"
        elif row["winner_dem"] == "1":
            uncontested = "Democrat"
        else:
            uncontested = "Republican"

        print(f"{year},{xx},{state},{district},{uncontested}")

    pass


if __name__ == "__main__":
    main()

### END ###
