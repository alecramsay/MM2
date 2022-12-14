#!/bin/bash
#
# Run MM2 for Congress script for many elections
#
# For example:
#
# scripts/run_batch.sh
#

echo "Running batch script ..."

scripts/apportion_seats.py --cycle 1990 -l 1
scripts/apportion_seats.py --cycle 2000 -l 1
scripts/apportion_seats.py --cycle 2010 -l 1
scripts/apportion_seats.py --cycle 2020 -l 1

# scripts/assign_seats.py -c 1990 -e 2000 -s 600 -l 1

# scripts/assign_seats.py -c 2000 -e 2002 -s 600 -l 1
# scripts/assign_seats.py -c 2000 -e 2004 -s 600 -l 1
# scripts/assign_seats.py -c 2000 -e 2006 -s 600 -l 1
# scripts/assign_seats.py -c 2000 -e 2008 -s 600 -l 1
# scripts/assign_seats.py -c 2000 -e 2010 -s 600 -l 1

# scripts/assign_seats.py -c 2010 -e 2012 -s 600 -l 1
# scripts/assign_seats.py -c 2010 -e 2014 -s 600 -l 1
# scripts/assign_seats.py -c 2010 -e 2016 -s 600 -l 1
# scripts/assign_seats.py -c 2010 -e 2018 -s 600 -l 1
# scripts/assign_seats.py -c 2010 -e 2020 -s 600 -l 1

# scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 600 -l 0
# scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 600 -l 1
# scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 650 -l 0
# scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 650 -l 1

echo "... done"
