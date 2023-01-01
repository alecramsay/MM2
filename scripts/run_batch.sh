#!/bin/bash
#
# Run MM2 for Congress script for many elections
#
# For example:
#
# scripts/run_batch.sh
#

echo "Running batch script"

scripts/do_apportionment.py --cycle 1990
scripts/do_apportionment.py --cycle 2000
scripts/do_apportionment.py --cycle 2010
scripts/do_apportionment.py --cycle 2020

echo "Done"
