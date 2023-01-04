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

option: str = "e"
strategy: int = 8

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

    ### DO SOMETHING ###

    ## Apportion seats ##

    # max_seats: int = 700
    # baseapp: HH_Apportioner = HH_Apportioner(census)
    # baseapp.log_priority_queue(max_seats)
    # app: MM2Apportioner = MM2Apportioner(
    #     census, None, list_min=list_min, total_seats=size, verbose=verbose
    # )
    # app.apportion_seats()

    ## Assign seats ##

    app: MM2Apportioner = MM2Apportioner(
        census, elections, list_min=list_min, total_seats=size, verbose=verbose
    )
    app.apportion_and_assign_seats()

    ## Strategy 8 ##

    # app: MM2ApportionerSandbox = MM2ApportionerSandbox(census, elections, verbose)
    # app.list_min = list_min
    # app.total_seats = size
    # app._r: int = 1
    # app.strategy8(size=size, option=option)

    ## Strategy N ##

    # app: MM2ApportionerSandbox = MM2ApportionerSandbox(census, elections, verbose)
    # app.eliminate_gap(strategy=strategy)

    pass


if __name__ == "__main__":
    main()

### END ###
