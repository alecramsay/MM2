#!/bin/bash
#
# Run MM2 for Congress script for many elections
#
# For example:
#
# scripts/apportion_ALL.sh
#

# TODO - Add # reps to apportion

echo "Apportioning 1990 census ..."
scripts/apportion_seats.py -c 1990 -r 601 -l 1
# scripts/apportion_seats.py -c 1990 -r 601 -l 0

echo "Apportioning 2000 census ..."
scripts/apportion_seats.py -c 2000 -r 601 -l 1
# scripts/apportion_seats.py -c 2000 -r 601 -l 0

echo "Apportioning 2010 census ..."
scripts/apportion_seats.py -c 2010 -r 601 -l 1
# scripts/apportion_seats.py -c 2010 -r 601 -l 0

echo "Apportioning 2020 census ..."
scripts/apportion_seats.py -c 2020 -r 601 -l 1
# scripts/apportion_seats.py -c 2020 -r 601 -l 0

echo "... done"
