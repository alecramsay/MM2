#!/bin/bash
#
# Run MM2 for Congress script for many elections
#
# For example:
#
# scripts/run_batch.sh
#

echo "Running batch script"

scripts/do_MM2_strategy_8_LOCAL.py -c 2020 -e 2022 -s 600 -o a
scripts/do_MM2_strategy_8_LOCAL.py -c 2020 -e 2022 -s 600 -o e
scripts/do_MM2_strategy_8_LOCAL.py -c 2020 -e 2022 -s 650 -o a
scripts/do_MM2_strategy_8_LOCAL.py -c 2020 -e 2022 -s 650 -o e

echo "Done"
