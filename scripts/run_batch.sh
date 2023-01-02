#!/bin/bash
#
# Run MM2 for Congress script for many elections
#
# For example:
#
# scripts/run_batch.sh
#

echo "Running batch script"

scripts/apportion_seats.py --cycle 1990
scripts/apportion_seats.py --cycle 2000
scripts/apportion_seats.py --cycle 2000
scripts/apportion_seats.py --cycle 2020

# scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 600 -l 0
# scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 600 -l 1
# scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 650 -l 0
# scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 650 -l 1

echo "Done"
