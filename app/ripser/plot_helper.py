import numpy as np
import matplotlib.pyplot as plt
from persim import plot_diagrams


def drawLineColored(X, C):
    for i in range(X.shape[0] - 1):
        plt.plot(X[i:i + 2, 0], X[i:i + 2, 1], c=C[i, :], lineWidth=3)


def plotCocycle2D(D, X, cocycle, thresh):
    """
    Given a 2D point cloud X, display a cocycle projected
    onto edges under a given threshold "thresh"
    """
    # Plot all edges under the threshold
    N = X.shape[0]
    t = np.linspace(0, 1, 10)
    c = plt.get_cmap('Greys')
    C = c(np.array(np.round(np.linspace(0, 255, len(t))), dtype=np.int32))
    C = C[:, 0:3]

    for i in range(N):
        for j in range(N):
            if D[i, j] <= thresh:
                Y = np.zeros((len(t), 2))
                Y[:, 0] = X[i, 0] + t * (X[j, 0] - X[i, 0])
                Y[:, 1] = X[i, 1] + t * (X[j, 1] - X[i, 1])
                drawLineColored(Y, C)
    # Plot cocycle projected to edges under the chosen threshold
    for k in range(cocycle.shape[0]):
        [i, j, val] = cocycle[k, :]
        if D[i, j] <= thresh:
            [i, j] = [min(i, j), max(i, j)]
            a = 0.5 * (X[i, :] + X[j, :])
            plt.text(a[0], a[1], '%g' % val, color='b')
    # Plot vertex labels
    for i in range(N):
        plt.text(X[i, 0], X[i, 1], '%i' % i, color='r')

    plt.axis('equal')
    plt.title("1-Form Thresh=%g" % thresh)
    # plt.show()
    plt.savefig(f"./figures/cocycles_thresh_{thresh}.png")
    plt.close()


def plot_diagrams_with_mark(diagrams: list, index, name: str):
    diagram_1 = diagrams[1]

    plot_diagrams(diagrams, show=False)
    plt.scatter(diagram_1[index, 0], diagram_1[index, 1], 20, 'k', 'x')
    plt.title("Max 1D birth = %.3g, death = %.3g" % (diagram_1[index, 0], diagram_1[index, 1]))
    # plt.show()
    plt.savefig(f"./figures/{name}_persistence_diagram.png")
    plt.close()


def plot_with_circular_coordinates(data: np.ndarray, circular_coordinates: list, name: str):
    plt.scatter(data[:, 0], data[:, 1], c=circular_coordinates, cmap='rainbow')
    plt.axis('equal')
    # plt.show()
    plt.savefig(f"./figures/{name}_with_coordinates.png")
    plt.close()

