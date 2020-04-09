from time import sleep

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from sklearn.decomposition import PCA

from app.ripser.ripser_utils import get_circular_data, apply_rips_circular, to_distance_matrix, apply_rips_torus, \
    apply_rips_object, apply_rips_merged_objects


def main():
    N = 20
    p = 41
    # X = get_circular_data(N, 0.4)
    #
    # np.random.seed(4)
    # apply_rips_circular(X, p, 'circle_20', plot_cycles=True)
    #
    # N = 100
    # X = get_circular_data(N, 0.2)
    # apply_rips_circular(X, p, 'circle_100')
    #
    # N = 15
    #
    # t = np.linspace(0, 1, N)
    # x, y = np.meshgrid(t, t)
    # x = np.reshape(x, (N * N, 1))
    # y = np.reshape(y, (N * N, 1))
    # X = np.hstack([x, y]) + 0.05 * np.random.random((N * N, 2))
    # X = X % 1
    #
    # D = to_distance_matrix(X)
    # apply_rips_torus(X, D, p)

    images = load_images()
    object = 4

    object_image_list = images[object]['original']
    flat_object_image_list = images[object]['flat']
    circular_coordinates = apply_rips_object(flat_object_image_list, p)

    # for i in range(len(object_image_list)):
    #     plt.imshow(object_image_list[i], cmap='gray')
    #     plt.title(f"Image {i} with circular coordinate {np.round(circular_coordinates[i], 4)}")
    #     # plt.show()
    #     plt.savefig(f"./figures/object_{object}_nr_{i}.png")
    #     plt.close()

    merged_flat_images = []
    for im in images.values():
        merged_flat_images += im['flat']

    merged_images = []
    for im in images.values():
        merged_images += im['original']

    circular_coordinates_merged = apply_rips_merged_objects(merged_flat_images, p)

    # for i in range(len(merged_images)):
    #     plt.imshow(merged_images[i], cmap='gray')
    #     plt.title(f"Image {i} with circular coordinate {np.round(circular_coordinates_merged[i], 4)}")
    #     # plt.show()
    #     plt.savefig(f"./figures/merged_nr_{i}.png")
    #     plt.close()


def load_images() -> dict:
    images = {}
    directory = './coil-20-unproc'

    for obj in range(1, 6):
        object_images = []
        flat_object_images = []

        for nr in range(72):
            im_frame = Image.open(f"{directory}/obj{obj}__{nr}.png")
            object_images.append(np.array(im_frame))
            # define a matrix
            pca = PCA(2)
            pca.fit(np.array(im_frame))
            projection = pca.transform(np.array(im_frame))
            # print(projection)
            flat_object_images.append(np.array(im_frame.getdata()))

        images[obj] = {
            'original': object_images,
            'flat': flat_object_images,
        }

    return images


if __name__ == '__main__':
    main()
