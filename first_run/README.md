# Reproducing Results
## Installing funsearch
To reproduce the results in this folder, you'll first have to setup funsearch on your local machine. 
1. Set up python and a good text editor for coding on your computer 
2. Clone the open source fun search repository and follow the setup instructions from the README on https://github.com/kitft/funsearch. Note, mistralai<2.0.0 is missing from requirements.txt, you should add this line to the file before spinning up a docker instance or installing the required dependencies. 
3. After creating a .env file, you should use the API key Eric gave us (contact Pablo if you weren't here on 7/9, when Eric gave us the API key) and set OPENROUTER_API_KEY=(key here) in the .env file.  
4. (Optional) Setup a wandb account and get your associated API key and then add the API key to .env as WANDB_API_KEY=(key here). This will make the results easier to parse. 
## Running an experiment 
Once you have funsearch setup, you can download the file "WS_perfect_info_float_spec.py" from the GitHub, put it in the examples file in funsearch and run the command 
```bash 
python -m funsearch runasync examples/WS_perfect_info_float_spec.py n --sandbox ExternalProcessSandbox --model deepseek-chat --envfile .env 
```
replacing n with whatever number of sets you'd like the partition to be in. 
I believe this will work in docker, although I have (unsafely) been running funsearch straight on my machine. 