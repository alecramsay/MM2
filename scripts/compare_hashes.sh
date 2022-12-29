#!/bin/bash
#
#  Compare hashes for Strategy 8a implementations - They should match
#
# For example:
#
# scripts/compare_hashes.sh
#

echo "Comparing hashes for Strategy 8a ..."

cd results
echo $PWD

shasum -a 256 "2022_reps_by_priority(8).csv" > "2022_reps_hash(8).txt"
shasum -a 256 "2022_reps_by_priority(8a).csv" >> "2022_reps_hash(8).txt"
shasum -a 256 "2022_reps_by_state(8).csv" >> "2022_reps_hash(8).txt"
shasum -a 256 "2022_reps_by_state(8a).csv" >> "2022_reps_hash(8).txt"

cd ..

echo "... done."