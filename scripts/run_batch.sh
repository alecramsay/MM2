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
scripts/apportion_seats.py --cycle 2010
scripts/apportion_seats.py --cycle 2020

echo "Done"
