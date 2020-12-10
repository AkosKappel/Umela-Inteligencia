__author__ = 'Akos Kappel'
__version__ = '1.0'

from matplotlib import pyplot as plt
# from sklearn.cluster import KMeans, AgglomerativeClustering
# import pandas as pd
import numpy as np
import random
import time


def generate_random_dots(count: int, min_range=-5000, max_range=5000):
    return [(random.randint(min_range, max_range), random.randint(min_range, max_range)) for _ in range(count)]


def generate_dataset(n_main_dots: int, n_nearby_dots: int):
    dots = generate_random_dots(n_main_dots)
    min_offset, max_offset = -100, 100
    for _ in range(n_nearby_dots):
        dot = random.choice(dots)
        x_offset, y_offset = random.randint(min_offset, max_offset), random.randint(min_offset, max_offset)
        new_dot = (dot[0] + x_offset, dot[1] + y_offset)
        dots.append(new_dot)
    return dots


def euclidean_distance(point_a, point_b):
    return int(np.sqrt((point_b[0] - point_a[0]) ** 2 + (point_b[1] - point_a[1]) ** 2))


def manhattan_distance(point_a, point_b):
    return abs(point_b[0] - point_a[0]) + abs(point_b[1] - point_a[1])


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
            dist = euclidean_distance(dot, centroid)
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
        centroid = (int(sum(x)/length), int(sum(y)/length))
        centroids.append(centroid)
    return centroids


def k_means_centroid(dots: list, k: int):
    prev_centroids = generate_random_dots(k)
    clusters = assign_clusters(dots, prev_centroids)

    while True:
        # plot_clusters(clusters, prev_centroids)
        centroids = calculate_centroids(clusters)
        n_empty_clusters = len(prev_centroids) - len(centroids)
        if n_empty_clusters != 0:
            new_centroids = generate_random_dots(n_empty_clusters)
            centroids.extend(new_centroids)

        clusters = assign_clusters(dots, centroids)
        if not any(euclidean_distance(prev_centroids[i], centroids[i]) > 50 for i in range(len(centroids))):
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
            dist_sum = sum(euclidean_distance(dot, other_dot) for other_dot in cluster)
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
        if not any(euclidean_distance(prev_medoids[i], medoids[i]) > 50 for i in range(len(medoids))):
            break
        prev_medoids = medoids

    return medoids, clusters


def calculate_distance_matrix(dots):
    matrix = []
    append = matrix.append
    for i, dot in enumerate(dots):
        append([manhattan_distance(dot, dots[j]) for j in range(i)])
    return matrix


def find_closest_dots(distance_matrix):
    min_dist = np.inf
    index_1, index_2 = None, None

    for i, row in enumerate(distance_matrix):
        for j, num in enumerate(row):
            if num < min_dist:
                min_dist = num
                index_1, index_2 = i, j

    return index_1, index_2


def calculate_centroid(*dots):
    x, y = list(zip(*dots))
    length = len(x)
    return int(sum(x)/length), int(sum(y)/length)


def agglomerative_clustering(dots: list, k: int):
    clusters = [[dot] for dot in dots]
    dist_matrix = calculate_distance_matrix(dots)

    for _ in range(len(dots) - k):
        index_1, index_2 = find_closest_dots(dist_matrix)
        dist_matrix[index_1].pop(index_2)  # Odstranime najmensiu najdenu vzdialenost

        distance_1 = dist_matrix.pop(index_1)
        for i in range(index_1, len(dist_matrix)):
            distance_1.append(dist_matrix[i].pop(index_1))

        distance_2 = dist_matrix.pop(index_2)
        for i in range(index_2, len(dist_matrix)):
            distance_2.append(dist_matrix[i].pop(index_2))

        new_row = [min(d1, distance_2[i]) for i, d1 in enumerate(distance_1)]
        dist_matrix.append(new_row)

        # Spojime dva klastre do jedneho
        cluster_1, cluster_2 = clusters.pop(index_1), clusters.pop(index_2)
        clusters.append(cluster_1 + cluster_2)

    return clusters


def get_cluster_size(cluster):
    try:
        x, y = map(list, zip(*cluster))
    except ValueError:  # Prazdny klaster
        return 0

    x.sort()
    y.sort()

    main_diagonal = euclidean_distance((x[0], y[-1]), (x[-1], y[0]))  # Z laveho horneho rohu do praveho dolneho
    anti_diagonal = euclidean_distance((x[-1], y[-1]), (x[0], y[0]))  # Z praveho horneho rohu do laveho dolneho

    intra_cluster_size = max(main_diagonal, anti_diagonal)
    return intra_cluster_size


def get_largest_cluster(clusters):
    largest = None
    max_size = 0

    for cluster in clusters:
        size = get_cluster_size(cluster)
        if size > max_size:
            max_size = size
            largest = cluster

    return largest


def divisive_clustering(dots: list, k: int):
    clusters = [dots]

    while len(clusters) < k:
        cluster = get_largest_cluster(clusters)
        index = clusters.index(cluster)
        clusters.remove(cluster)

        _, cluster = k_means_centroid(cluster, 2)
        clusters.insert(index, cluster[0])
        clusters.append(cluster[-1])
        # plot_clusters(clusters)

    return clusters


def main():
    random.seed(99)
    dots = generate_dataset(20, 5000)

    start = time.time()
    # centers, clusters = k_means_centroid(dots, 11)
    centers, clusters = k_means_medoid(dots, 11)
    plot_clusters(clusters, centers)

    # clusters = agglomerative_clustering(dots, 11)
    # clusters = divisive_clustering(dots, 7)
    # plot_clusters(clusters)

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
