#!/bin/bash
#
# Run MM2 for Congress script for many elections
#
# For example:
#
# scripts/run_batch.sh
#

echo "Running batch script"

echo "Seats per state for 1990 census"
scripts/multiple_seats.py --cycle 1990

echo "Seats per state for 2000 census"
scripts/multiple_seats.py --cycle 2000

echo "Seats per state for 2010 census"
scripts/multiple_seats.py --cycle 2010

echo "Seats per state for 2020 census"
scripts/multiple_seats.py --cycle 2020

echo "Done"
