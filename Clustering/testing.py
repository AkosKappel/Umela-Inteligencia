import numpy as np
import random
import time


def test1():
    t = time.time()
    print('Test 1:', time.time() - t)


def test2():
    t = time.time()
    print('Test 2:', time.time() - t)


def manhattan_distance(point_a, point_b):
    return abs(point_b[0] - point_a[0]) + abs(point_b[1] - point_a[1])


def show(arr):
    for num in arr:
        print(num)
    print()


# random.seed(10)
# dots = [(random.randint(0, 10_000), random.randint(0, 10_000)) for _ in range(1_000_000)]

test1()
test2()
