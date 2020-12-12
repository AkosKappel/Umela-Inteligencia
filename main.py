__author__ = 'Akos Kappel'

from matplotlib import pyplot as plt
from typing import List, Tuple
import numpy as np
import random
import time


def generate_random_dots(count: int, min_range=-5000, max_range=5000) -> List[Tuple[int, int]]:
    """
    Generuje zoznam nahodnych bodov.

    :param count: pocet bodov
    :param min_range: minimalna mozna hodnota pre suradnice
    :param max_range: maximalna mozna hodnota pre suradnice
    :return: zoznam bodov
    """
    return [(random.randint(min_range, max_range), random.randint(min_range, max_range)) for _ in range(count)]


def generate_dataset(n_main_dots: int, n_nearby_dots: int) -> List[Tuple[int, int]]:
    """
    Vytvori dataset s nahodnymi bodmi.

    :param n_main_dots: pocet hlavnych nahodnych bodov
    :param n_nearby_dots: pocet bodov, ktore su v blizkosti hlavnych bodov
    :return: dataset
    """
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
    # 21 farieb pre vizualizaciu grafu
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

    if centers:  # Vyznaci krizikom centroidy alebo medoidy
        x, y = list(zip(*centers))
        plt.scatter(x, y, c='k', marker='x')

    if show_and_clear:
        plt.show()
        plt.clf()


def assign_clusters(dots, centers):  # Prideli kazdy bod k najblizsiemu centroidu alebo medoidu
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


def get_plane_resolution(dots):  # Zisti minimalnu a maximalnu suradnicu bodov
    try:
        x, y = map(list, zip(*dots))
    except ValueError:  # Prazdny zoznam bodov
        return 0, 0
    return min(*x, *y), max(*x, *y)


def calculate_centroids(clusters):  # Vypocita centroidy klastrov
    centroids = []
    for cluster in clusters:
        try:
            x, y = list(zip(*cluster))
        except ValueError:  # Vynimka pre prazdne klastre
            continue
        length = len(x)
        centroid = (int(sum(x)/length), int(sum(y)/length))  # Aritmeticky priemer suradnic
        centroids.append(centroid)
    return centroids


def k_means(dots: list, k: int):  # K-means klastrovanie
    min_range, max_range = get_plane_resolution(dots)
    prev_centroids = generate_random_dots(k, min_range, max_range)
    clusters = assign_clusters(dots, prev_centroids)

    while True:
        # plot_clusters(clusters, prev_centroids)
        centroids = calculate_centroids(clusters)
        if len(centroids) != k:
            new_centroids = generate_random_dots(k - len(centroids), min_range, max_range)
            centroids.extend(new_centroids)

        clusters = assign_clusters(dots, centroids)
        if all(euclidean_distance(prev_centroids[i], centroid) < 100 for i, centroid in enumerate(centroids)) \
                and all(len(cluster) > 0 for cluster in clusters):
            break
        prev_centroids = centroids

    return centroids, clusters


def choose_medoids(dots, count, min_distance=300):  # Vyberie body ktore su od seba vzdialene aspon o urcitu vzdialenost
    while True:
        medoids = random.sample(dots, count)
        for medoid in medoids:
            if any(euclidean_distance(medoid, other_medoid) < min_distance
                   for other_medoid in medoids if other_medoid != medoid):
                break
        else:
            break
    return medoids


def calculate_medoids(clusters):  # Vypocita medoidy klastrov
    medoids = []
    inf = np.inf

    for cluster in clusters:
        min_distance_sum = inf
        medoid = None

        for dot in cluster:
            dist_sum = sum(manhattan_distance(dot, other_dot) for other_dot in cluster)
            if dist_sum < min_distance_sum:
                min_distance_sum = dist_sum
                medoid = dot  # Bod s najmensim suctom vzdialensti od ostatnch bodov v klastri

        medoids.append(medoid)
    return medoids


def k_medoids(dots: list, k: int):  # K-medoids klastrovanie
    prev_medoids = choose_medoids(dots, k)
    clusters = assign_clusters(dots, prev_medoids)

    while True:
        # plot_clusters(clusters, prev_medoids)
        medoids = calculate_medoids(clusters)
        clusters = assign_clusters(dots, medoids)
        if all(euclidean_distance(prev_medoids[i], medoid) < 100 for i, medoid in enumerate(medoids)):
            break
        prev_medoids = medoids

    return medoids, clusters


def calculate_distance_matrix(dots):  # Vypocita maticu so vzdialenostami medzi vsetkymi bodmi
    matrix = []
    append = matrix.append
    for i, dot in enumerate(dots):
        append([manhattan_distance(dot, dots[j]) for j in range(i)])
    return matrix


def find_closest_dots(distance_matrix):  # Najde najmensiu vzdialenost v matici
    min_dist = np.inf
    index_1, index_2 = None, None

    for i, row in enumerate(distance_matrix):
        try:
            dist = min(row)
        except ValueError:  # Vynimka pre prazdny zoznam
            continue
        if dist < min_dist:
            min_dist = dist
            index_1, index_2 = i, row.index(dist)  # Poradove cisla najblizsich bodov

    return index_1, index_2


def calculate_centroid(*dots):
    x, y = list(zip(*dots))
    length = len(x)
    return int(sum(x)/length), int(sum(y)/length)


def agglomerative_clustering(dots: list, k: int):  # Aglomerativne zhlukovanie
    clusters = [[dot] for dot in dots]
    dist_matrix = calculate_distance_matrix(dots)

    for _ in range(len(dots) - k):
        index_1, index_2 = find_closest_dots(dist_matrix)  # Najde najblizsie klastre
        dist_matrix[index_1].pop(index_2)  # Odstrani najmensiu najdenu vzdialenost medzi klastrami

        distance_1 = dist_matrix.pop(index_1)
        distance_1.extend([dist_matrix[i].pop(index_1) for i in range(index_1, len(dist_matrix))])

        distance_2 = dist_matrix.pop(index_2)
        distance_2.extend([dist_matrix[i].pop(index_2) for i in range(index_2, len(dist_matrix))])

        new_row = [min(d1, distance_2[i]) for i, d1 in enumerate(distance_1)]  # Aktualizuje vzdialenosti v matici
        dist_matrix.append(new_row)

        cluster_1, cluster_2 = clusters.pop(index_1), clusters.pop(index_2)  # Spoji dva klastre do jedneho
        clusters.append(cluster_1 + cluster_2)

    return clusters


def get_cluster_size(cluster):  # Vypocita najvacsiu vzdialenost medzi bodmi v klastri
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


def get_largest_cluster(clusters):  # Najde najvacsi klaster
    largest = None
    max_size = 0

    for cluster in clusters:
        size = get_cluster_size(cluster)
        if size > max_size:
            max_size = size
            largest = cluster

    return largest


def divisive_clustering(dots: list, k: int):  # Divizivne zhlukovanie
    clusters = [dots]

    while len(clusters) < k:
        cluster = get_largest_cluster(clusters)
        index = clusters.index(cluster)
        clusters.remove(cluster)

        _, cluster = k_means(cluster, 2)  # Rozdeli najvasci klaster na 2 mensie
        clusters.insert(index, cluster[0])
        clusters.append(cluster[-1])
        # plot_clusters(clusters)

    return clusters


def set_clustering_method() -> int:
    print('Vyberte ktory algoritmus sa ma pouzit na klastrovanie:',
          '1 - k-means',
          '2 - k-medoids',
          '3 - aglomerativne zhlukovanie',
          '4 - divizivne zhlukovanie', sep='\n')

    while True:
        clustering_method = input('Zadajte cislo moznosti > ')
        try:
            clustering_method = int(clustering_method)
            if clustering_method in (1, 2, 3, 4):
                break
            raise ValueError
        except ValueError:
            print(f'Zvolena moznost {clustering_method} neexistuje.')

    return clustering_method


def set_k() -> int:
    while True:
        k = input('Zadajte hodnotu K > ')
        try:
            k = int(k)
            if k > 0:
                break
            raise ValueError
        except ValueError:
            print('Zvolena hodnota K musi byt kladne cele cislo.')
    return k


def scale_down(dots, scale_factor=50):  # Zmensi rozsah a pocet bodov
    x, y = list(zip(*dots))
    x = list(map(lambda n: int(n/scale_factor), x))
    y = list(map(lambda n: int(n/scale_factor), y))
    return list(set(zip(x, y)))


def scale_up(dots, scale_factor=50):  # Zvacsi rozsah bodov
    x, y = list(zip(*dots))
    x = list(map(lambda n: n * scale_factor, x))
    y = list(map(lambda n: n * scale_factor, y))
    return list(zip(x, y))


def reconstruct_image(dots, clusters, scale_factor=50):  # Pomocou zmenseneho rozsahu priradi vsetky body do klastrov
    final_clusters = [[] for _ in range(len(clusters))]

    for dot in dots:
        repr_dot = int(dot[0]/scale_factor), int(dot[1]/scale_factor)
        for i, cluster in enumerate(clusters):
            if repr_dot in cluster:
                final_clusters[i].append(dot)
                break

    return final_clusters


def get_correct_clusters_count(clusters, centers):  # Vyhodnoti uspesnost klastrovania
    n_successful_clusters = 0

    for i, cluster in enumerate(clusters):
        dist_sum = sum(euclidean_distance(dot, centers[i]) for dot in cluster)
        avg_distance = int(dist_sum / len(cluster))

        if avg_distance <= 500:  # Uspesny klaster ma priemernu vzdialenost bodov od stredu maximalne 500
            n_successful_clusters += 1

    return n_successful_clusters


def main():
    random.seed(44)
    dataset = generate_dataset(20, 20_000)

    method = set_clustering_method()
    k = set_k()
    start = time.time()

    if method == 1:
        centers, clusters = k_means(dataset, k)

    elif method == 2:
        centers, clusters = k_medoids(dataset, k)

    elif method == 3:
        scaled_dataset = scale_down(dataset)
        clusters = agglomerative_clustering(scaled_dataset, k)
        clusters = reconstruct_image(dataset, clusters)
        centers = calculate_centroids(clusters)

    elif method == 4:
        clusters = divisive_clustering(dataset, k)
        centers = calculate_centroids(clusters)

    else:
        clusters, centers = [], []

    end = time.time()
    n_correct_cluster = get_correct_clusters_count(clusters, centers)
    success_rate = n_correct_cluster * 100 / len(clusters)

    print(f'Uspesnost klastrovania: {success_rate:.2f} %',
          f'Pocet uspesnych klastrov: {n_correct_cluster}',
          f'Cas trvania algoritmus: {end - start:.2f} s', sep='\n')
    plot_clusters(clusters, centers)


if __name__ == '__main__':
    main()
