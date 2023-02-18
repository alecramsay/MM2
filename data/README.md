# Data

## Census Data

These came from:
 
- https://www.census.gov/data/tables/1990/dec/1990-apportionment-data.html
- https://www.census.gov/data/tables/2000/dec/2000-apportionment-data.html (Table 1)
- https://www.census.gov/data/tables/2010/dec/2010-apportionment-data.html (Table 1)
- https://www.census.gov/data/tables/2020/dec/2020-apportionment-data.html (Table 1)

The oldest census available digitally is 1990. 
For 1970 and 1980, the reports were only available as PDF’s:

- https://www.census.gov/history/pdf/ApportionmentInformation-1970Census.pdf
- https://www.census.gov/history/pdf/ApportionmentInformation-1980Census.pdf

I downloaded these, scraped the data into spreadsheets, and then converted them to CSV’s.

## Election Results

Initially, election results came from the [US House](https://github.com/alecramsay/ushouse) and
incorporate imputed results for uncontested elections.

The format for each election was a CSV with the following columns:

- YEAR: year of the election
- STATE: friendly name of the state
- XX: two-letter state abbreviation
- REP_V: number of votes for the Republican candidates, with imputed results for uncontested elections
- DEM_V: number of votes for the Democratic candidates, with imputed results for uncontested elections
- OTH_V: number of votes for other non-major party candidates <<< not used
- TOT_V: total number of votes <<< not used
- REP_S: the number of Republican wins
- DEM_S: the number of Democratic wins
- OTH_S: the number of other non-major party wins
- TOT_S: the total number of seats <<< not used
- VOTE_%: the two-party Democratic vote share <<< not used
- SEAT_%: the two-party Democratic seat share <<< not used

To extend our analysis farther back in time, we switched over to use data from Chris Warshaw:

- Observed results in each congressional election since 1972 in every state. These are mostly from [Constituency-Level Elections Archive (CLEA)](https://electiondataarchive.org). The 2022 election data are from the Cook Political Report.
- Chris' imputations for each election based on the approach described in the appendix of his [LSQ paper](https://onlinelibrary.wiley.com/action/downloadSupplement?doi=10.1111%2Flsq.12276&file=lsq12276-sup-0001-Supinfo.pdf) with Nick Stephanopoulos.
- Data on incumbency and presidential vote (Democratic two-party share) in each district, generously shared by Gary Jacobson (see [paper](https://www.journals.uchicago.edu/doi/abs/10.1086/681670).