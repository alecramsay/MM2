# MM2

Code for exploring Benjamin Plener Cover's [Two-Party Structural Countermandering](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3891735) (aka "MM2").

## Base Apportionment

The HH_Apportioner class implements the Huntington-Hill method used today to apportion representatives to states 
for the House based on a decennial census.
It takes a census data as input: a list of dicts read from a CSV by DictReader (using `read_csv()`).
Examples are in the data/census/ directory.
To apportion representatives to states based on a census, call the assign_first_N() method with a 435.

```python
app = HH_Apportioner(census)
app.assign_first_N(435)
```

The class generates a queue of priority values sorted in descending order, initially 100 entries per state.
You can continue to allocate seats to states, by calling the `assign_next()` method which returns
the # of the House seat, the priority value, the state that gets the seat, and the seat # for the state.

## Augmented Apportionment

The MM2Apportioner class wraps the HH_Apportioner class and adds functionality for apportioning addition (party)
list seats to states, again based on a decennial census, and then allocating the list seats to parties based
on the results of an election.
This can be used in two modes. To apportion nominal & list seats to states based on a census:

```python
app = MM2Apportioner(
    census, None, list_min=list_min, total_seats=size, verbose=verbose
)
app.apportion_seats()
```

The apportion_seats.py does this and writes results into a file named "{census year}_census_reps_by_state({size},{list minimum}).csv" into the results/ directory, where:

- {census year} is the year of the census data
- {size} is the total number of seats to apportion (both nominal & list), and
- {list minimum} is the minimum number of list seats guaranteed for each state (0 or 1)

To allocate the list seats apportioned to states to the parties based on election data:

```python
appr = MM2Apportioner(
    census, elections, list_min=list_min, total_seats=size, verbose=verbose
)
app.apportion_and_assign_seats()
```

The assign_seats.py scripts does and writes reports into the results/ directory:

1. {election year}_report({size},{list minimum}).txt summarizes the run.
2. {election year}_reps_by_state({size},{list minimum}).csv summarizes nominal & list seats by state.
[//]: # (3. {election year}_reps_by_priority({strategy}).csv shows the seat-by-seat assignments.)

where:
- {election year} is the year of the election data, and
- the other variables are as above

The logic of these two processes is described in [Logic](./notes/logic.md).

Our explorations of alternative MM2 apportionment strategies are described in [Explorations](./notes/explorations.md).