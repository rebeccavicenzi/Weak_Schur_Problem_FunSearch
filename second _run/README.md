## Methods Summary
This set of experiments makes two signifcant changes from the first. 
1. We calculate priority as tuples of floats (of length n) instead of just plain floats. This means we only call priority once for each integer, instead of n times. 
2. Instead of making our partition as big as possible, we set a target number of integers we'd like to put into the partition. 
3. At each step we choose the set/integer
2 is really just a necessity of 3. The idea behind change 3 is that giving the LLM the ability to choose the order in which the bins get filled might closer ressemble a human workflow and allow it to develop more complex heuristics. 
## Results Summary
Some themes in the LLM responses include:
1. Failure to recognize that direct conflicts are already dealt with by solve()...
2. Clustering bonuses (preferring sticking close integers together)
3. Balancing bin sizes
This run has failed to replicate any of the best known bounds although which is a regression from the previous run. However, this experiment has demonstrated that it is quite easy to create a large partition that is missing just a few critical numbers. 
This feature might be the reason for the run's failure: as it is relatively easy to fill up the partition most of the way, there is little partial progress for the LLM to make towards its goal. This stalls out the genetic algorithm and leaves us hoping that the 'random' noise in the functional space that the LLM provides will make a large jump in quality. 
If the genetic algorithm performed worse because the evaluate function was less continuous, then our goal should be to make the evaluate function more continuous. Maybe this could be done by making the problem 'harder' for the LLM in some respect or spreading out the hardest bit of creating a large partition across a large number of scores. 
