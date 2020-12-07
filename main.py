__author__ = 'Akos Kappel'
__version__ = '1.0'

from matplotlib import pyplot as plt
# from sklearn.cluster import KMeans
# import pandas as pd
import numpy as np
import random
import time


min_value, max_value = -5000, 5000  # Interval suradnic nahodnych bodov v 2D priestore
min_offset, max_offset = -100, 100  # Interval odchylok od ostatnych bodov


def generate_random_dots(count: int):
    return [(random.randint(min_value, max_value), random.randint(min_value, max_value)) for _ in range(count)]


def generate_dataset(n_main_dots: int, n_close_dots: int):
    dots = generate_random_dots(n_main_dots)
    for _ in range(n_close_dots):
        dot = random.choice(dots)
        x_offset, y_offset = random.randint(min_offset, max_offset), random.randint(min_offset, max_offset)
        new_dot = (dot[0] + x_offset, dot[1] + y_offset)
        dots.append(new_dot)
    return dots  # list(zip(*dots))


def distance(point_a, point_b):
    return np.sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)


def assign_clusters(dots, centroids):
    clusters = [[] for _ in range(len(centroids))]
    inf = np.inf

    for dot in dots:
        min_distance = inf
        index = 0

        for i, centroid in enumerate(centroids):
            dist = distance(dot, centroid)
            if dist < min_distance:
                min_distance = dist
                index = i

        clusters[index].append(dot)
    return clusters


def calculate_centroids(clusters):
    centroids = []
    for cluster in clusters:
        try:
            x, y = list(zip(*cluster))
        except ValueError:
            continue
        centroid = (sum(x)/len(x), sum(y)/len(y))
        centroids.append(centroid)
    return centroids


def kmeans_centroid(dots: list, k: int):
    centroids = generate_random_dots(k)
    clusters = assign_clusters(dots, centroids)

    for _ in range(8):
        centroids = calculate_centroids(clusters)
        clusters = assign_clusters(dots, centroids)

    return centroids, clusters


def main():
    random.seed(41186)
    start = time.time()

    dots = generate_dataset(20, 40_000)
    centroids, clusters = kmeans_centroid(dots, 20)

    for cluster in clusters:
        x, y = list(zip(*cluster))
        plt.scatter(x, y)

    x, y = list(zip(*centroids))
    plt.scatter(x, y, c='k', marker='x')

    print(time.time() - start)
    plt.show()


# data = pd.read_csv('dataset2.csv')
# X = data.iloc[:, [0, 1]].values
# X = np.array([[5, 3], [10, 15], [15, 12], [24, 10], [30, 45],
#               [85, 70], [71, 80], [60, 78], [55, 52], [80, 91]])
# X = np.array(create_points(20, 40_000))

# kmeans = KMeans(n_clusters=7)
# kmeans.fit(X)
# plt.scatter(x, y, cmap='rainbow')


if __name__ == '__main__':
    main()
