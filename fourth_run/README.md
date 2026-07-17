## Results
The most inspiring results from this round of changes is WS$(5) \geq 195$, which is one off of the best known lower bound on WS$(5)$. This is a particularly hopeful outcome as, unlike WS$(4)$ and WS$(3)$, there is no known upper bound on WS$(5)$ and beating WS$(5) \geq 196$ would dissprove a 74 year-old conjecture of G.W. Walker. 
## Changes Made
There were 2 primary changes made.
1. Multiple LLMs were used (deepseek v4 flash preview, llama 4 scout and mistral small 2603)
2. Prompt engineering changes.
The latter changes were based on a few observations on past funsearch runs. Namely, there were a few heuristics the LLM followed that seemed consistently succesful. To speed up rediscovery, these observations were added as a hint in the docstring of the priority function. By adding these to the prompt, we run the risk of narrowing the LLMs purview. To counterbalance this, the system prompt was edited slightly in a few places to encourage more ambitious changes to the code. 