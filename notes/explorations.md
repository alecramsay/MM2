# Explorations

This note summarizes our explorations into alternative strategies for assigning list seats to states.

## MM2 for Congress

The MM2ApportionerSandbox class wraps the HH_Apportioner class and adds MM2 for Congress functionality.
In addition to the census data, this takes election data in a similar form: a list of dicts read from a CSV by DictReader.
Examples are in the data/election/ directory.
To assign list seats to states based on the election data, call the eliminate_gap() method with a strategy.

```python
app = MM2ApportionerSandbox(census, elections)
app.eliminate_gap(strategy=strategy)
```

We explored 8 strategies for eliminating the gap:
1. Minimize the prospective skew for the state
2. Reduce the national gap 
3. Balance the two -- when the prospective skews would both be below a threshold, eliminate the national gap; otherwise minimize the state skew
4. Balance the two but define skew wrto a responsiveness = 2, i.e., efficiency gap = 0
5. Assign 50 list seats, reducing the national gap
6. Assign 165 list seats (600 total), balancing the two with skew(r=2) until gap is zero and then just minimize the national gap
7. Assign 165 list seats (600 total), balancing the two with skew(r=1) until gap is zero and then just minimize the national gap
8. Assign 165 list seats (600 total), always minimizing the prospective skew for the state

The explore_strategy_N.py script in the scripts/ directory takes a census decade, an election year, and a strategy, 
loads the census and election data, eliminates the national gap assigning list seats to states using the specified strategy:

```shell
scripts/explore_strategy_N.py 2010 2012 -s 3
```

The default strategy is 8.

When focused in on Strategy 8, I streamlined code for that in the MM2ApportionerSandbox class and exposed it in the
explore_strategy_8.py script:

```shell
scripts/explore_strategy_8.py -c 2010 -e 2020 -s 600 -o e
```

The script supports diffent total sizes (-s) and different guarantees of list seats to states (-o). Option 'a' is no guarantee; option 'e' guarantees at least one list seat per state..

These scritps write the results to three files:

1. {election year}_report({strategy}).txt summarizes the run.
2. {election year}_reps_by_priority({strategy}).csv shows the seat-by-seat assignments.
3. {election year}_reps_by_state({strategy}).csv summarizes nominal & list seats by state.

