
"""
Calculates the sum of the even values in the fibonacci
sequence below 4,000,000
"""
def calcFib():
    total = 0
    previous = 0
    current = 1
    while current < 4000000:
        previous, current = current, previous + current
        if current % 2 == 0:
            total += current
    print(total)

