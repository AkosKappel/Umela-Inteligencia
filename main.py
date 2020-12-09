__author__ = 'Akos Kappel'
__version__ = '1.0'

from matplotlib import pyplot as plt
from sklearn.cluster import KMeans, AgglomerativeClustering
import pandas as pd
import numpy as np
import random
import time


min_value, max_value = -5000, 5000  # Interval suradnic nahodnych bodov v 2D priestore
min_offset, max_offset = -100, 100  # Interval odchylok od ostatnych bodov


def generate_random_dots(count: int):
    return [(random.randint(min_value, max_value), random.randint(min_value, max_value)) for _ in range(count)]


def generate_dataset(n_main_dots: int, n_nearby_dots: int):
    dots = generate_random_dots(n_main_dots)
    for _ in range(n_nearby_dots):
        dot = random.choice(dots)
        x_offset, y_offset = random.randint(min_offset, max_offset), random.randint(min_offset, max_offset)
        new_dot = (dot[0] + x_offset, dot[1] + y_offset)
        dots.append(new_dot)
    return dots


def distance(point_a, point_b):
    return np.sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2)


def plot_clusters(clusters, centers=None, show_and_clear=True):
    index = 0
    colors = ('#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2',
              '#7f7f7f', '#bcbd22', '#17becf', '#ffe119', '#4363d8', '#911eb4', '#bcf60c',
              '#fabebe', '#000075', '#008080', '#e6beff', '#fffac8', '#800000', '#aaffc3')

    for cluster in clusters:
        try:
            x, y = list(zip(*cluster))
        except ValueError:  # Prazdny klaster
            continue
        plt.scatter(x, y, s=10, c=colors[index])
        index += 1
        index %= len(colors)

    if centers:
        x, y = list(zip(*centers))
        plt.scatter(x, y, c='k', marker='x')

    if show_and_clear:
        plt.show()
        plt.clf()


def assign_clusters(dots, centers):
    clusters = [[] for _ in range(len(centers))]
    inf = np.inf

    for dot in dots:
        min_distance = inf
        index = 0

        for i, centroid in enumerate(centers):
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
        except ValueError:  # Vynimka pre prazdne klastre
            continue
        length = len(x)
        centroid = (sum(x)/length, sum(y)/length)
        centroids.append(centroid)
    return centroids


def k_means_centroid(dots: list, k: int):
    prev_centroids = generate_random_dots(k)
    clusters = assign_clusters(dots, prev_centroids)

    while True:
        # plot_clusters(clusters, prev_centroids)
        centroids = calculate_centroids(clusters)
        clusters = assign_clusters(dots, centroids)
        if all(distance(prev_centroids[i], centroids[i]) < 50 for i in range(len(centroids))):
            break
        prev_centroids = centroids

    return centroids, clusters


def calculate_medoids(clusters):
    medoids = []
    inf = np.inf

    for cluster in clusters:
        min_distance_sum = inf
        medoid = None

        for dot in cluster:
            dist_sum = sum(distance(dot, other_dot) for other_dot in cluster)
            if dist_sum < min_distance_sum:
                min_distance_sum = dist_sum
                medoid = dot

        medoids.append(medoid)
    return medoids


def k_means_medoid(dots: list, k: int):
    prev_medoids = random.sample(dots, k)
    clusters = assign_clusters(dots, prev_medoids)

    while True:
        plot_clusters(clusters, prev_medoids)
        medoids = calculate_medoids(clusters)
        clusters = assign_clusters(dots, medoids)
        if not any(distance(prev_medoids[i], medoids[i]) > 50 for i in range(len(medoids))):
            break
        prev_medoids = medoids

    return medoids, clusters


def agglomerative_clustering(dots):
    clusters = [[dot] for dot in dots]


def divisive_clustering(dots):
    clusters = [dots]


def main():
    random.seed(44)
    dots = generate_dataset(20, 20_000)

    start = time.time()
    # centers, clusters = k_means_centroid(dots, 11)
    centers, clusters = k_means_medoid(dots, 11)

    plot_clusters(clusters, centers)
    print(time.time() - start)
    plt.show()


# t = time.time()
# data = pd.read_csv('dataset1.csv')
# X = data.iloc[:, [0, 1]].values
# kmeans = KMeans(n_clusters=11)
# kmeans.fit(X)
# y_kmeans = kmeans.predict(X)
# plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=10)
# print(time.time() - t)
# plt.show()
# exit(0)

if __name__ == '__main__':
    main()
