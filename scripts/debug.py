#!/usr/bin/env python3
#

"""
DEBUG 
"""

from MM2 import *


### ARGS ###

cycle: int = 2010
election: int = 2012
size: int = 600
list_min: int = 1
verbose: bool = False

### MODS FOR LOCAL USE ###

census_root: str = "data/census"
elections_root: str = "data/elections"


def main() -> None:

    ### LOAD THE CENSUS ###

    csv_data: str = "{}/{}_census.csv".format(census_root, cycle)
    types: list = [str, str, int]
    census: list = read_typed_csv(csv_data, types)

    ### LOAD THE ELECTION RESULTS ###

    csv_data: str = "{}/Congressional Elections ({}).csv".format(
        elections_root, election
    )
    types = [str] * 3 + [int] * 8 + [float] * 2
    elections: list = read_typed_csv(csv_data, types)

    ### APPORTION NOMINAL & LIST SEATS ###

    app: MM2Apportioner = MM2Apportioner(
        census, elections, list_min=list_min, total_seats=size, verbose=verbose
    )
    app.apportion_and_assign_seats()

    ### WRITE THE RESULTS ###

    pass


if __name__ == "__main__":
    main()

### END ###
