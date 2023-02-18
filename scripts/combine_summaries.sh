#!/bin/bash
#
# Combine all the summary records by option combination 
#
# For example, in the 'results' directory:
#
# ../scripts/combine_summaries.sh
#

cat summary_header.csv *_summary\(601\,1\).csv > summary\(601,1\).csv
