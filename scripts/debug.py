#!/usr/bin/env python3

"""
DEBUG 
"""

from MM2 import *


### ARGS ###

cycle: int = 1990
election: int = 1998
size: int = 601
list_min: int = 1

verbose: bool = False

census_root: str = "data/census"
elections_root: str = "data/elections"


def main() -> None:
    ### LOAD THE CENSUS ###

    csv_data: str = "{}/{}_census.csv".format(census_root, cycle)
    types: list = [str, str, int]
    census: list = read_csv(csv_data, types)

    ### LOAD THE ELECTION RESULTS ###

    csv_data: str = "{}/Congressional Elections ({}).csv".format(
        elections_root, election
    )
    types = [str] * 3 + [int] * 5
    # types = [str] * 3 + [int] * 8 + [float] * 2
    elections: list = read_csv(csv_data, types)

    ## Apportion & assign seats ##

    app: MM2Apportioner = MM2Apportioner(
        census, elections, list_min=list_min, total_seats=size, verbose=verbose
    )
    app.apportion_and_assign_seats()

    pass


if __name__ == "__main__":
    main()

### END ###
