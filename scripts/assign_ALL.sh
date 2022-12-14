#!/bin/bash
#
# Run MM2 for Congress script for many elections
#
# For example:
#
# scripts/assign_ALL.sh
#

echo "Running batch script ..."

echo "Assigning list seats for 2000 election ..."
scripts/assign_seats.py -c 1990 -e 2000 -s 601 -l 0
scripts/assign_seats.py -c 1990 -e 2000 -s 601 -l 1
scripts/assign_seats.py -c 1990 -e 2000 -s 651 -l 0
scripts/assign_seats.py -c 1990 -e 2000 -s 651 -l 1

echo "Assigning list seats for 2002 election ..."
scripts/assign_seats.py -c 2000 -e 2002 -s 601 -l 0
scripts/assign_seats.py -c 2000 -e 2002 -s 601 -l 1
scripts/assign_seats.py -c 2000 -e 2002 -s 651 -l 0
scripts/assign_seats.py -c 2000 -e 2002 -s 651 -l 1

echo "Assigning list seats for 2004 election ..."
scripts/assign_seats.py -c 2000 -e 2004 -s 601 -l 0
scripts/assign_seats.py -c 2000 -e 2004 -s 601 -l 1
scripts/assign_seats.py -c 2000 -e 2004 -s 651 -l 0
scripts/assign_seats.py -c 2000 -e 2004 -s 651 -l 1

echo "Assigning list seats for 2006 election ..."
scripts/assign_seats.py -c 2000 -e 2006 -s 601 -l 0
scripts/assign_seats.py -c 2000 -e 2006 -s 601 -l 1
scripts/assign_seats.py -c 2000 -e 2006 -s 651 -l 0
scripts/assign_seats.py -c 2000 -e 2006 -s 651 -l 1

echo "Assigning list seats for 2008 election ..."
scripts/assign_seats.py -c 2000 -e 2008 -s 601 -l 0
scripts/assign_seats.py -c 2000 -e 2008 -s 601 -l 1
scripts/assign_seats.py -c 2000 -e 2008 -s 651 -l 0
scripts/assign_seats.py -c 2000 -e 2008 -s 651 -l 1

echo "Assigning list seats for 2010 election ..."
scripts/assign_seats.py -c 2000 -e 2010 -s 601 -l 0
scripts/assign_seats.py -c 2000 -e 2010 -s 601 -l 1
scripts/assign_seats.py -c 2000 -e 2010 -s 651 -l 0
scripts/assign_seats.py -c 2000 -e 2010 -s 651 -l 1

echo "Assigning list seats for 2012 election ..."
scripts/assign_seats.py -c 2010 -e 2012 -s 601 -l 1
scripts/assign_seats.py -c 2010 -e 2012 -s 601 -l 0
scripts/assign_seats.py -c 2010 -e 2012 -s 651 -l 0
scripts/assign_seats.py -c 2010 -e 2012 -s 651 -l 1

echo "Assigning list seats for 2014 election ..."
scripts/assign_seats.py -c 2010 -e 2014 -s 601 -l 0
scripts/assign_seats.py -c 2010 -e 2014 -s 601 -l 1
scripts/assign_seats.py -c 2010 -e 2014 -s 651 -l 0
scripts/assign_seats.py -c 2010 -e 2014 -s 651 -l 1

echo "Assigning list seats for 2016 election ..."
scripts/assign_seats.py -c 2010 -e 2016 -s 601 -l 0
scripts/assign_seats.py -c 2010 -e 2016 -s 601 -l 1
scripts/assign_seats.py -c 2010 -e 2016 -s 651 -l 0
scripts/assign_seats.py -c 2010 -e 2016 -s 651 -l 1

echo "Assigning list seats for 2018 election ..."
scripts/assign_seats.py -c 2010 -e 2018 -s 601 -l 0
scripts/assign_seats.py -c 2010 -e 2018 -s 601 -l 1
scripts/assign_seats.py -c 2010 -e 2018 -s 651 -l 0
scripts/assign_seats.py -c 2010 -e 2018 -s 651 -l 1

echo "Assigning list seats for 2020 election ..."
scripts/assign_seats.py -c 2010 -e 2020 -s 601 -l 0
scripts/assign_seats.py -c 2010 -e 2020 -s 601 -l 1
scripts/assign_seats.py -c 2010 -e 2020 -s 651 -l 0
scripts/assign_seats.py -c 2010 -e 2020 -s 651 -l 1

echo "Assigning list seats for 2022 election ..."
scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 601 -l 1
scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 601 -l 0
scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 651 -l 0
scripts/assign_seats_LOCAL.py -c 2020 -e 2022 -s 651 -l 1

echo "... done"
