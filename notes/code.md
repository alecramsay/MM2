# Implementation Notes

Implementing the apportion_seats.py script highlighted that the total # of seats apportioned 
to each state is stable for a redistricting cycle: it only depends on the census which is
the same for the decade. Each election can change the D/R mix of the list seats assigned to
the state though.

My initial implementation (MM2ApportionerSandbox) allowed us to explore alternative assignment & termination rules.
It generated the priority queue and assigned seats to state _and_ parties at the same time.
Given a specific strategy -- e.g., 435 nominal seats, 165 list (600 total) and always minimize
state skew -- a cleaner more transparent implementation would re-factor this into two distinct
processes:

1. Generate the priority queue & assign seats to states (nominal vs. list) -- This is the same
  for every election in the decade.

2. Assign list seats to parties within each state -- Iterate over the states and allocate the
  list seats to the parties in each state minimizing the skew in the state delegation.

Re-factoring in this way (MM2Apportioner) made the final code much more tranparent.