# MM2

Code for exploring Benjamin Plener Cover's [Two-Party Structural Countermandering](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3891735) (aka "MM2").

## Congressional Apportionment

The HH_Apportioner class implements the Huntington-Hill method used to apportion the representatives to states for the US Congress.
It takes a census data as input: a list of dicts read from a CSV by DictReader (see `read_typed_csv()`).
Examples are in the data/census/ directory.
To apportion representatives to states based on a census, call the assign_first_N() method with a 435.

```python
app = HH_Apportioner(census)
app.assign_first_N(435)
```

## MM2 for Congress

The MM2_Apportioner class wraps the HH_Apportioner class and adds MM2 for Congress functionality.
In addition to the census data, this takes election data in a similar form: a list of dicts read from a CSV by DictReader.
Examples are in the data/election/ directory.
To assign list seats to states based on the election data, call the eliminate_gap() method with a strategy.

```python
app = MM2_Apportioner(census, elections)
app.eliminate_gap(strategy=strategy)
```

There are three strategies for eliminating the gap:
1. Minimize the prospective skew for the state
2. Reduce the national gap 
3. Balance the two -- when the prospectives skews would both be below a threshold, eliminate the national gap; otherwise minimize the state skew.