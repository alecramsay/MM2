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

shasum -a 256 "2022_reps_by_state(600,0).csv" > "2022_hash.txt"
shasum -a 256 "2022_reps_by_state(600,1).csv" >> "2022_hash.txt"
shasum -a 256 "2022_reps_by_state(650,0).csv" >> "2022_hash.txt"
shasum -a 256 "2022_reps_by_state(650,1).csv" >> "2022_hash.txt"

cd explorations
echo $PWD

shasum -a 256 "2022_reps_by_state(8a,600).csv" > "2022_hash.txt"
shasum -a 256 "2022_reps_by_state(8e,600).csv" >> "2022_hash.txt"
shasum -a 256 "2022_reps_by_state(8a,650).csv" >> "2022_hash.txt"
shasum -a 256 "2022_reps_by_state(8e,650).csv" >> "2022_hash.txt"

cd ..

echo "... done."