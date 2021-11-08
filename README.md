## Running implemented solutions 
Solutions for problems 1 & 6 are implemented in the `spatial_challenges` package <br>
as `problem1.py` and `problem6.py` respectively

Calls to both and prints of their runtimes are made from `invocation.py`. 

To ensure the solutions run as expected simply run:
```
python3 invocation.py
```
in this directory.


### Side notes on other challenges (not solved for sake of time)
- **Challenge 3**: Can be solved using dynamic programming (with memoization)
- **Challenge 4**: Hexagonal is a proper subset of Triangular so next value would just be the next one that is Triangular and Pentagonal (save time on Hexagonal check)