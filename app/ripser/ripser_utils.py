import numpy as np
import matplotlib.pyplot as plt
from persim import plot_diagrams
from ripser import ripser

from app.ripser.plot_helper import plotCocycle2D, plot_diagrams_with_mark, plot_with_circular_coordinates


def calculate_circular_coordinates(distance_matrix: np.ndarray, cocycle: np.array, threshold: float, p: int) -> list:
    # Take the subset of the cocycle where the distance of the vertices is smaller than the threshold

    smaller_than_threshold_keys = (distance_matrix[cocycle[:, 0], cocycle[:, 1]] <= threshold)
    cocycle_r = cocycle[smaller_than_threshold_keys]
    cocycle_lift_r = lift(cocycle_r, p)

    # Create sample coboundary matrix by creating a zero matrix of N columns and an amount of rows
    # equal to the amount of edges in cocycle_lift_r

    M = np.zeros((cocycle_lift_r.shape[0], distance_matrix.shape[0]))

    for k in range(cocycle_lift_r.shape[0]):
        [i, j, evaluation] = cocycle_lift_r[k, :]

        M[k, i] = 1
        M[k, j] = -1

    M_inv = np.linalg.pinv(M)

    return list(np.dot(M_inv, - cocycle_lift_r[:, 2]) % 1)


def get_circular_data(nr_of_points: int, noise: float) -> np.array:
    t = np.linspace(0, 2 * 3.1415, nr_of_points, endpoint=False)

    return np.transpose([np.cos(t), np.sin(t)]) + noise * np.random.random((nr_of_points, 2))


def lift(cocycle: np.ndarray, p: int) -> np.ndarray:
    shifted_mod_p = cocycle[:, 2] - p * (cocycle[:, 2] > (p - 1) // 2)

    return np.array([cocycle[:, 0], cocycle[:, 1], shifted_mod_p]).T


def apply_rips_circular(
        data: np.array,
        p: int,
        name: str,
        distance_matrix: bool = False,
        plot_cycles: bool = False,
        plot_scatter: bool = False
    ):
    result = ripser(X=data, coeff=p, do_cocycles=True, distance_matrix=distance_matrix)
    D, diagrams, cocycles = result['dperm2all'], result['dgms'], result['cocycles']

    diagram = diagrams[1]
    index = np.argmax(diagram[:, 1] - diagram[:, 0])

    plot_diagrams_with_mark(diagrams, index, name)

    threshold = diagram[index, 1] - 0.001
    cocycle = cocycles[1][index]

    circular_coordinates = calculate_circular_coordinates(D, cocycle, threshold, p)

    if plot_scatter:
        plot_with_circular_coordinates(data, circular_coordinates, name)

    if plot_cycles:
        plotCocycle2D(D, data, cocycle, diagram[index, 1])
        plotCocycle2D(D, data, cocycle, diagram[index, 1] - 0.0001)
        plotCocycle2D(D, data, cocycle, diagram[index, 0] + 0.0001)


def to_distance_matrix(data: np.ndarray):
    N = data.shape[0]
    D = np.zeros((N, N))

    for i in range(N):
        for j in range(i, N):
            distance = np.linalg.norm(data[i] - data[j])

            if distance <= 0.5:
                D[i, j] = D[j, i] = distance
                continue

            options = [np.linalg.norm(data[i] - y) for y in [
                data[j] + [0, 1],
                data[j] + [1, 0],
                data[j] + [1, 1],
                data[j] + [1, -1],
                data[j] - [0, 1],
                data[j] - [1, 0],
                data[j] - [1, 1],
                data[j] - [1, -1],
            ]
                       ]

            D[i, j] = D[j, i] = min(options + [distance])

    return D


def apply_rips_torus(data: np.ndarray, distance_matrix: np.ndarray, p: int):
    result = ripser(
        X=distance_matrix,
        maxdim=1,
        coeff=p,
        do_cocycles=True,
        distance_matrix=True
    )
    D, diagrams, cocycles = result['dperm2all'], result['dgms'], result['cocycles']

    diagram_1 = diagrams[1]
    index_1 = np.argmax(diagram_1[:, 1] - diagram_1[:, 0])

    diagram_minus_persistent_pt = np.copy(diagram_1)
    diagram_minus_persistent_pt[index_1] = np.array([0, 0])
    index_2 = np.argmax(diagram_minus_persistent_pt[:, 1] - diagram_minus_persistent_pt[:, 0])

    plot_diagrams(diagrams, show=False)
    plt.scatter(diagram_1[index_1, 0], diagram_1[index_1, 1], 20, 'k', 'x')
    plt.scatter(diagram_1[index_2, 0], diagram_1[index_2, 1], 20, 'k', 'x')
    # plt.title("Max 1D birth = %.3g, death = %.3g" % (diagram_1[index_1, 0], diagram_1[index_1, 1]))
    # plt.show()
    plt.savefig(f"./figures/flat_torus_persistence_diagram.png")

    threshold = min(diagram_1[index_1, 1], diagram_1[index_2, 1]) - 0.001

    cocycle1 = cocycles[1][index_1]
    circular_coordinates1 = calculate_circular_coordinates(D, cocycle1, threshold, p)
    plot_with_circular_coordinates(data, circular_coordinates1, 'flat_torus_1')

    cocycle2 = cocycles[1][index_2]
    circular_coordinates2 = calculate_circular_coordinates(D, cocycle2, threshold, p)
    plot_with_circular_coordinates(data, circular_coordinates2, 'flat_torus_2')


def euclidean_distance_matrix(data: np.ndarray):
    N = data.shape[0]
    D = np.zeros((N, N))

    for i in range(N):
        for j in range(i, N):
            distance = np.linalg.norm(data[i] - data[j])
            D[i, j] = D[j, i] = distance

    return D


def apply_rips_object(flat_images, p: int):
    D = euclidean_distance_matrix(np.array(flat_images))

    result = ripser(
        X=D,
        maxdim=1,
        coeff=p,
        do_cocycles=True,
        distance_matrix=True
    )

    return result_to_circular_coordinates(result, p)


def result_to_circular_coordinates(result, p: int):
    D, diagrams, cocycles = result['dperm2all'], result['dgms'], result['cocycles']

    diagram_1 = diagrams[1]
    index = np.argmax(diagram_1[:, 1] - diagram_1[:, 0])

    # plot_diagrams_with_mark(diagrams, index, 'object')

    threshold = diagram_1[index, 1] - 0.001
    cocycle = cocycles[1][index]

    return calculate_circular_coordinates(D, cocycle, threshold, p)


def apply_rips_merged_objects(flat_images, p: int):
    D = euclidean_distance_matrix(np.array(flat_images))

    result = ripser(
        X=D,
        maxdim=1,
        coeff=p,
        do_cocycles=True,
        distance_matrix=True
    )

    D, diagrams, cocycles = result['dperm2all'], result['dgms'], result['cocycles']

    diagram_1 = diagrams[1]
    indices = np.argsort((diagram_1[:, 1] - diagram_1[:, 0])/diagram_1[:, 0])

    plot_diagrams(diagrams, show=False)
    plt.savefig(f"./figures/merged_persistence_diagram.png")
    plt.close()

    threshold = min([diagram_1[index, 1] for index in indices[-5:]]) - 0.001

    for index in indices[-5:]:
        cocycle = cocycles[1][index]
        circular_coordinates = calculate_circular_coordinates(D, cocycle, threshold, p)


    threshold = diagram_1[index, 1] - 0.001
    cocycle_1 = cocycles[1][index_1]
    cocycle_2 = cocycles[1][index_2]
    cocycle_3 = cocycles[1][index_3]
    cocycle_4 = cocycles[1][index_4]
    cocycle_5 = cocycles[1][index_5]

    return calculate_circular_coordinates(D, cocycle, threshold, p)