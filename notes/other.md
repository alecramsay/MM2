# "Other" votes/seats

## MM2ApportionerSandbox

**Initializer**

- Calls MM2ApportionerBase initializer
- Then calls _abstract_byState_data() and _sum_national_totals()

**Assignment**

- Strategy 8 ...

TODO: What is updating self.N with each iteration?

**Post processing**

- Calls _calc_analytics() which calculates power & skew, using byState s, n, v, t, s', and n' 

TODO: Do these handle "other" properly?

## MM2Apportioner

**Initializer** 

- Just calls MM2ApportionerBase initializer

**Assignment**

- apportion_and_assign_seats() calls _abstract_election_data() and _sum_national_totals()
- Then it calls apportion_seats() and assign_party_mix()
- apportion_seats() calls apportion_nominal_seats() which, in turn calls _abstract_census_data()

TODO: Make sure the component abstract-data methods handle "other" votes & seats correctly.

TODO: Make sure _sum_national_totals() handles "other" votes & seats correctly. This is used by both legacy & new code paths.

**Post processing**

- _calc_skew() and _calc_power() are split across the apportionment and assignment steps.

TODO: Make sure they handle "other" votes & seats correctly.

## Totals

Make sure "other" (non-D/R) votes & seats are being handled correctly.

Three places that process election data (_elections).

### _abstract_byState_data()

This is a legacy combo used by the sandbox code. It abstracts both census and election data. It's called in set_elections (first).

TODO: Where is this data used?

### _sum_national_totals()

Called in set_election (second).

- The D votes (V) and two-party votes (T) for an election correctly remove "other" votes.
- The D seats (S) and two-party seats (N) for an election correctly remove "other" seats.
- The nominal D seats (S0) and total seats (N0) correctly snapshot their respective nominal values.

TODO: How does N in _sum_national_totals() relate to the seat # being apportioned?

### _abstract_election_data() 

Instead of the legacy _abstract_byState_data(), production calls unbundled _abstract_census_data() and _abstract_election_data() individually.

- The former is called in apportion_nominal_seats() which is called in apportion_seats().
- The latter is called in apportion_and_assign_seats(). It's called first and the followed by calls to apportion_seats() and assign_party_mix().

## Test cases

TODO
 