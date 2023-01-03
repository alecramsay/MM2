The [MM2](https://github.com/alecramsay/MM2) repository houses code for exploring applying
Benjamin Plener Cover's [Two-Party Structural Countermandering](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3891735) 
to Congress (aka "MM2 for Congress" or simply "MM2").

MM2 apportions additional list seats to states based on the census and then distributes them
to the two major parties (Democrats and Republicans) based on the results of a congressional election,
to reduce the deviation from proportional representation in the House.

To apportion nominal & list seats based on a decennial census:

- Apportion the 435 nominal seats as today
- Then apportion the additional list seats in priority order
- Until the remaining list seats are needed to ensure that every state gets at least one list seat (if guaranteed), and
- Then (if so) assign the remaining seats to states with no list seats 

To assign a state's list seats to parties based on a congressional election:

- If a state has no list seats, neither party gets a list seat (of course)
- If a state has one or more list seats, compute the gap between the number nominal seats Democrats won and the number of seats closest to proportional representation for the total number of seats apportioned to the state (i.e., nominal + list), given the two-party Democratic vote share
- The number of list seats for Democrats is the maximum of the gap and zero (they can't *lose* seats) and the minimum of that an the number of list seats (they can't get *more* than were apportioned to the state)
- The number of list seats for Republicans is the total number of list seats minus the number assigned to Democrats

 This minimizes the deviation from proportional representation for each state's congressional delegation.
 
 Note: There's no preferential treatment for Democrats: you can reverse the order, if you like.