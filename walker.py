#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A Random Walk Simulation For Multiple Walkers"""


# Python code for 2D random walk.
# Source: https://www.geeksforgeeks.org/random-walk-implementation-python/
import sys
import numpy as np
import matplotlib.pyplot as plt


def create_walkers(number_of_steps, number_of_walkers):
    """
    Creates a list of numpy arrays which each hold the coordinates of a walker. The coordinates
    are randomly chosen in a range from 0 to the number of steps
    :param number_of_steps: the number of steps the walker will make. This defines the
    dimension of the array which represents the walker
    :param number_of_walkers: the number of walkers defines the number of arrays, which
    will be created
    :return: a list, the 'scene' which contains all walkers, so all arrays containing coordinates
    """
    scene = []
    for _ in range(number_of_walkers):
        # create the array of a walker and add it to the scene-list
        walker = np.random.randint(low=0, high=number_of_steps,
                                    size=(number_of_steps, 2))
        scene.append(walker)

    return scene


def calculate_the_path(walker, number_of_steps):
    """
    Calculates the path the walker walks
    :param walker: The array representing the walker, holding random coordinates
    :param number_of_steps: the number of steps the walker takes
    :return: the updated array representing the walker, holding all coordinates the walker walks to
    """
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
    Creates the plot of the calculated path of the walker
    :param list_of_walkers: Arrays representing the walkers. Each array holds the
    coordinates of the respective path the walker walked.
    :param outputfilename: The file which will be created with the plotted paths
    """
    # define the number of rows and columns of subplots
    if len(list_of_walkers) == 1:
        columns_of_plots = 1
    else:
        columns_of_plots = 2
    rows_of_plots = round(len(list_of_walkers)/2)

    # create the subplots
    figure, axis = plt.subplots(rows_of_plots, columns_of_plots)
    for counter in enumerate(list_of_walkers):
        # get the coordinates of this walker, get its subplot and plot the path in it
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
        # if the number of walkers is odd, delete the last (unused) subplot
        figure.delaxes(axis[(rows_of_plots - 1), 1])

    # arange subplot to not interfere each other, save the figure to the outputfile and
    # show the plot to the user
    figure.tight_layout()
    plt.savefig(outputfilename)
    plt.show()


def main():
    """The main program. Reads in the user definitions, creates the scene, calculates
    the path and plots it"""
    try:
        # read in specifications defined by the user
        number_of_steps = int(sys.argv[1]) + 1
        number_of_walkers = int(sys.argv[2])
        outputfilename = sys.argv[3]

        assert number_of_steps > 1, "number_of_steps must be greater than '0'. " \
                                    "You stated '{}'".format(number_of_steps - 1)
        assert number_of_walkers > 0, "number_of_walkers must be greater than '1'. " \
                                      "You stated '{}'".format(number_of_walkers)
        assert number_of_walkers <= 12, "number_of_walkers must be max. '12'. " \
                                        "You stated '{}'".format(number_of_walkers)
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
        walker = calculate_the_path(walker, number_of_steps)
    plot_the_paths(scene, outputfilename)


if __name__ == "__main__":
    main()
