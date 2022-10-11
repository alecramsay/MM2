# MM2

Code for exploring Benjamin Plener Cover's [Two-Party Structural Countermandering](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3891735) (aka "MM2").

## Congressional Apportionment

The HH_Apportioner class implements the Huntington-Hill method used to apportion the representatives to states for the US Congress.
It takes a census data as input: a list of dicts read from a CSV by DictReader (using `read_typed_csv()`).
Examples are in the data/census/ directory.
To apportion representatives to states based on a census, call the assign_first_N() method with a 435.

```python
app = HH_Apportioner(census)
app.assign_first_N(NOMINAL_SEATS)
```

The class generates a queue of priority values sorted in descending order, initially 100 entries per state.
You can continue to allocate seats to states, by calling the `assign_next()` method which returns
the # of the House seat, the priority value, the state that gets the seat, and the seat # for the state.

## MM2 for Congress

The MM2_Apportioner class wraps the HH_Apportioner class and adds MM2 for Congress functionality.
In addition to the census data, this takes election data in a similar form: a list of dicts read from a CSV by DictReader.
Examples are in the data/election/ directory.
To assign list seats to states based on the election data, call the eliminate_gap() method with a strategy.

```python
app = MM2_Apportioner(census, elections)
app.eliminate_gap(strategy=strategy)
```

There are 7 strategies for eliminating the gap:
1. Minimize the prospective skew for the state
2. Reduce the national gap 
3. Balance the two -- when the prospective skews would both be below a threshold, eliminate the national gap; otherwise minimize the state skew
4. Balance the two but define skew wrto a responsiveness = 2, i.e., efficiency gap = 0
5. Assign 50 list seats, reducing the national gap
6. Assign 165 list seats (600 total), balancing the two with skew(r=2) until gap is zero and then just minimize the national gap
7. Assign 165 list seats (600 total), balancing the two with skew(r=1) until gap is zero and then just minimize the national gap
8. Assign 165 list seats (600 total), always minimizing the prospective skew for the state

The MM2_for_Congress.py script in the scripts/ directory takes a census decade, an election year, and a strategy, 
loads the census and election data, eliminates the national gap assigning list seats to states using the specified strategy:

```shell
scripts/MM2_for_Congress.py 2010 2012 -s 3
```

The default strategy is 8.

It writes the results to three files:

1. {election year}_report({strategy}).txt summarizes the run.
2. {election year}_reps_by_priority({strategy}).csv shows the seat-by-seat assignments.
3. {election year}_reps_by_state({strategy}).csv summarizes nominal & list seats by state.

## TODO

If 3rd-party or independent represenatives win more seats, we may need to revisit the calculations.
The national targets are two-party vote and seat shares.
The total # of nominal seats by state ('n') includes all apportioned seats though.