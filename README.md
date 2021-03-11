# MS


Persistent Random Search:

The code is used for simulating different kinds of search algorithms in a closed environment. The search agent is allowed to move in four directions in the closed environment:
North, East, South and West. The goal of the search agent is to find and eat as many food nodes as possible. The simulation is more focused on finding out what kind of moving strategy is best at searching through an unknown environment. The moving strategy consists of deciding what direction the agent should move next and how big of a step should it take. The agent also has a 'sight' radius, meaning that if a food node is within the agent's sight radius, the agent no longer chooses his next direction randomly but rather converges to the closest food node.
There are 3 types of strategies used for deciding the next direction:
1 - Uniformly distributed probability of moving in each direction
2 - Backtracking strategy - the probability of going back to a place where the agent came from is lowered. (Only one previous step is considered)
    Ex. If the agent's previous action was going EAST, the probabilities for the next action for going north, east, south and west are 0.3, 0.3, 0.3, 0.1 respectively.
3 - Forward Checking and Backtracking strategy - the name is a bit ambiguous since the algorithm isn't actually checking forwards to its relative position, it just means that the agent has an increased probability of moving in his relative 'forwards' direciton.
    Ex. If the agent's previous action was going EAST, the probabilities for the next action for going north, east, south and west are 0.25, 0.4, 0.25, 0.1 respectively.

There are 3 types of strategies used for deciding each step size:
1 - Uniform step size set to 1 coordinate points
2 - Step size determined by a sample from a Gaussian distribution
3 - Step size determined by a sample from an Exponential distribution

The statistical measurements used to compare the relative 'score' of any two strategies are:
- Food collected in 50, 100, 200 and 500 steps
- Steps until the agent finds a single food node
