#!/bin/bash
#
# Run MM2 for Congress script for many elections
#
# For example:
#
# scripts/run_batch.sh
#

echo "Running batch script"

# echo "2000 ..."
# scripts/MM2_for_Congress.py 1990 2000 -s 8 -r

# echo "2002 ..."
# scripts/MM2_for_Congress.py 2000 2002 -s 8 -r

# echo "2004 ..."
# scripts/MM2_for_Congress.py 2000 2004 -s 8 -r

# echo "2006 ..."
# scripts/MM2_for_Congress.py 2000 2006 -s 8 -r

# echo "2008 ..."
# scripts/MM2_for_Congress.py 2000 2008 -s 8 -r

# echo "2010 ..."
# scripts/MM2_for_Congress.py 2000 2010 -s 8 -r

# echo "2012 ..."
# scripts/MM2_for_Congress.py 2010 2012 -s 8 -r

# echo "2014 ..."
# scripts/MM2_for_Congress.py 2010 2014 -s 8 -r

# echo "2016 ..."
# scripts/MM2_for_Congress.py 2010 2016 -s 8 -r

# echo "2018 ..."
# scripts/MM2_for_Congress.py 2010 2018 -s 8 -r

# echo "2020 ..."
# scripts/MM2_for_Congress.py 2010 2020 -s 8 -r

echo "2022 ..."
scripts/MM2_for_Congress_LOCAL.py 2020 2022 -s 8 -r 

echo "Done"
