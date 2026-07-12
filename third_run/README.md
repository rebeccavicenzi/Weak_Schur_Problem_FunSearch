## Summary of Changes
This spec is identical to spec1 except
1. The system prompt was updated to provide more information on what weakly sum free partitions are
2. Functions that act similarily (score wise) to the 0.0 base function are sent to 0. This encourages more substantive changes at the start of runs. 
## Summary of Results
We've rediscovered WS(4) >= 66 and gotten marginally better results for higher n values. Additionally, the system seems to improve quicker, perhaps as a result of change #2. 
Also, I tried using other models (e.g. llama scout and mistral small) and ran into troubles where the eval queue grows large and nothing gets evaluated. I tried turning down the max eval time but it doesn't seem to have helped. 