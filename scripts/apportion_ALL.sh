#!/bin/bash
#
# Run MM2 for Congress script for many elections
#
# For example:
#
# scripts/apportion_ALL.sh
#

echo "Apportioning 1990 census ..."
scripts/apportion_seats.py --cycle 1990 -l 1
scripts/apportion_seats.py --cycle 1990 -l 0

echo "Apportioning 2000 census ..."
scripts/apportion_seats.py --cycle 2000 -l 1
scripts/apportion_seats.py --cycle 2000 -l 0

echo "Apportioning 2010 census ..."
scripts/apportion_seats.py --cycle 2010 -l 1
scripts/apportion_seats.py --cycle 2010 -l 0

echo "Apportioning 2020 census ..."
scripts/apportion_seats.py --cycle 2020 -l 1
scripts/apportion_seats.py --cycle 2020 -l 0

echo "... done"
