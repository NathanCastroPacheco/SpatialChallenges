import time
from spatial_challenges import problem1, problem6

c1_start_time = time.time()
problem1.calculateP1WinCount()
print(f'Problem 1 Solved in: {(time.time() - c1_start_time) * 1000} ms')

c6_start_time = time.time()
problem6.calcFib()
print(f'Problem 6 Solved in: {(time.time() - c6_start_time) * 1000} ms')


