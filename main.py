#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A Random Walk Simulation """


# Python code for 2D random walk.
# Source: https://www.geeksforgeeks.org/random-walk-implementation-python/
import sys
import numpy as np
import matplotlib.pyplot as plt


def create_walkers(number_of_steps, number_of_walkers):
    """

    :param number_of_steps:
    :param number_of_walkers:
    :return:
    """
    scene = []
    for _ in range(number_of_walkers):
        walker = np.random.randint(low=0, high=number_of_steps,
                                    size=(number_of_steps, 2))
        scene.append(walker)

    return scene


def do_the_steps(walker, number_of_steps):
    """the main program"""
    # split coordinates
    x_coord = walker[:, 0]
    y_coord = walker[:, 1]

    # calculate new coordinates for each step
    for stepnumber in range(1, number_of_steps):
        direction_of_step = np.random.randint(1, 4)
        if direction_of_step == 1:      # east
            x_coord[stepnumber] = x_coord[stepnumber - 1] + 1
            y_coord[stepnumber] = y_coord[stepnumber - 1]
        elif direction_of_step == 2:    # west
            x_coord[stepnumber] = x_coord[stepnumber - 1] - 1
            y_coord[stepnumber] = y_coord[stepnumber - 1]
        elif direction_of_step == 3:    # north
            x_coord[stepnumber] = x_coord[stepnumber - 1]
            y_coord[stepnumber] = y_coord[stepnumber - 1] + 1
        else:                           # south
            x_coord[stepnumber] = x_coord[stepnumber - 1]
            y_coord[stepnumber] = y_coord[stepnumber - 1] - 1

    # return all coordinates of the path
    return walker


def plot_the_paths(list_of_walkers, outputfilename):
    """

    :param list_of_walkers:
    :param outputfilename:
    :return:
    """
    if len(list_of_walkers) == 1:
        columns_of_plots = 1
    else:
        columns_of_plots = 2
    rows_of_plots = round(len(list_of_walkers)/2)
    figure, axis = plt.subplots(rows_of_plots, columns_of_plots)
    for counter in enumerate(list_of_walkers):
        x_coords = counter[1][:, 0]
        y_coords = counter[1][:, 1]

        row = int(counter[0]/2)
        if counter[0] % 2 == 0:
            column = 0
        else:
            column = 1

        axis[row, column].plot(x_coords, y_coords)
        axis[row, column].set_title(f'Walker {counter[0]+1}')

    if len(list_of_walkers) % 2 != 0:
        figure.delaxes(axis[(rows_of_plots - 1), 1])


    figure.tight_layout()
    plt.savefig(outputfilename)
    plt.show()


def main():
    """

    :return:
    """
    try:
        number_of_steps = int(sys.argv[1]) + 1
        number_of_walkers = int(sys.argv[2])
        outputfilename = sys.argv[3]

        assert number_of_steps > 1
        assert number_of_walkers > 0
    except ValueError as err:
        print("Error: one of the inputs was not correctly specified.\n"
              "The Input must be specified as 'python main.py number_of_steps "
              "number_of_walkers outputfilename'.\n"
              "Inputformats: number_of_steps --> Integer, number_of_walkers --> "
              "Integer, outputfilename --> string\n"
              "outputfilename: path_to_output/filename.png\n"
              "The number of walkers and the number of steps to be made must be "
              "positive & at least 1\n\n\n",
              err)
        sys.exit(1)

    scene = create_walkers(number_of_steps, number_of_walkers)
    for walker in scene:
        walker = do_the_steps(walker, number_of_steps)
    plot_the_paths(scene, outputfilename)


if __name__ == "__main__":
    main()
