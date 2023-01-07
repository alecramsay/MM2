#!/bin/bash
#
# Combine all the summary records by option combination 
#
# For example, in results/:
#
# ../scripts/combine_summaries.sh
#

cat summary_header.csv 2000_summary\(601,0\).csv 2002_summary\(601,0\).csv 2004_summary\(601,0\).csv 2006_summary\(601,0\).csv 2008_summary\(601,0\).csv 2010_summary\(601,0\).csv 2012_summary\(601,0\).csv 2014_summary\(601,0\).csv 2016_summary\(601,0\).csv 2018_summary\(601,0\).csv 2020_summary\(601,0\).csv 2022_summary\(601,0\).csv > summary\(601,0\).csv

cat summary_header.csv 2000_summary\(601,1\).csv 2002_summary\(601,1\).csv 2004_summary\(601,1\).csv 2006_summary\(601,1\).csv 2008_summary\(601,1\).csv 2010_summary\(601,1\).csv 2012_summary\(601,1\).csv 2014_summary\(601,1\).csv 2016_summary\(601,1\).csv 2018_summary\(601,1\).csv 2020_summary\(601,1\).csv 2022_summary\(601,1\).csv > summary\(601,1\).csv

cat summary_header.csv 2000_summary\(651,0\).csv 2002_summary\(651,0\).csv 2004_summary\(651,0\).csv 2006_summary\(651,0\).csv 2008_summary\(651,0\).csv 2010_summary\(651,0\).csv 2012_summary\(651,0\).csv 2014_summary\(651,0\).csv 2016_summary\(651,0\).csv 2018_summary\(651,0\).csv 2020_summary\(651,0\).csv 2022_summary\(651,0\).csv > summary\(651,0\).csv

cat summary_header.csv 2000_summary\(651,1\).csv 2002_summary\(651,1\).csv 2004_summary\(651,1\).csv 2006_summary\(651,1\).csv 2008_summary\(651,1\).csv 2010_summary\(651,1\).csv 2012_summary\(651,1\).csv 2014_summary\(651,1\).csv 2016_summary\(651,1\).csv 2018_summary\(651,1\).csv 2020_summary\(651,1\).csv 2022_summary\(651,1\).csv > summary\(651,1\).csv