__author__ = 'Akos Kappel'
__version__ = '1.0'

from matplotlib import pyplot as plt
# from sklearn.cluster import KMeans
# import pandas as pd
# import numpy as np
import random
import time


min_value, max_value = -5000, 5000  # Interval suradnic nahodnych bodov v 2D priestore
min_offset, max_offset = -100, 100  # Interval odchylok od ostatnych bodov


def generate_random_dots(count):
    return [(random.randint(min_value, max_value), random.randint(min_value, max_value)) for _ in range(count)]


def generate_dataset(n_main_dots: int, n_close_dots: int) -> list:
    dots = generate_random_dots(n_main_dots)
    for _ in range(n_close_dots):
        dot = random.choice(dots)
        x_offset, y_offset = random.randint(min_offset, max_offset), random.randint(min_offset, max_offset)
        new_dot = (dot[0] + x_offset, dot[1] + y_offset)
        dots.append(new_dot)
    return list(zip(*dots))  # dots


random.seed(41186)
start = time.time()

x, y = generate_dataset(20, 40_000)

# p = []
# with open('dataset1.csv', 'r') as f:
#     for line in f:
#         p += tuple(map(int, line.strip('\n').split(',')))
# print(p)

# generate_points(20, 40_000, 'dataset2.csv', seed=0)
# data = pd.read_csv('dataset2.csv')
# X = data.iloc[:, [0, 1]].values
# print(x)

# X = np.array([[5, 3], [10, 15], [15, 12], [24, 10], [30, 45],
#               [85, 70], [71, 80], [60, 78], [55, 52], [80, 91]])
# X = np.array(create_points(20, 40_000))

# kmeans = KMeans(n_clusters=7)
# kmeans.fit(X)
plt.scatter(x, y, cmap='rainbow')

# plt.scatter(x[20:], y[20:], s=1)
# plt.scatter(x[:20], y[:20], s=1, c='red')

print(time.time() - start)
plt.show()
