#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A Random Walk Simulation For Multiple Walkers"""

# Python code for 2D random walk.
# Source: https://www.geeksforgeeks.org/random-walk-implementation-python/
import sys
import math
import numpy as np
import matplotlib.pyplot as plt


def create_walkers(
    walking_time: int,
    number_of_usual_walkers: int,
    number_of_fast_walkers: int,
    number_of_running_walkers: int,
) -> list:
    """
    Creates a list of all walker objects.
    :param walking_time: the 'time' each walker walks and therefore (depending on it's
        respective speed) the number of steps the walker will make
    :param number_of_usual_walkers: the number of usual walkers defines the number of
        objects of this respective class which will be appended to the scene
    :param number_of_fast_walkers:the number of fast walkers defines the number of
        objects of this respective class which will be appended to the scene
    :param number_of_running_walkers: the number of running walkers defines the number
        of objects of this respective class which will be appended to the scene
    :return: a list, the 'scene' which contains all walkers, so all objects and their
        coordinates
    """
    scene = []
    for _ in range(number_of_usual_walkers):
        # create the array of a walker and add it to the scene-list
        scene.append(UsualWalker(walking_time))
    for _ in range(number_of_fast_walkers):
        # create the array of a walker and add it to the scene-list
        scene.append(FastWalker(walking_time))
    for _ in range(number_of_running_walkers):
        # create the array of a running walker and add it to the scene-list
        scene.append(RunningWalker(walking_time))
    return scene


def calculate_the_path(number_of_steps: int) -> tuple:
    """
    Calculates the path the walker walks
    :param number_of_steps: the number of steps the walker takes
    :return: all x- and all y- coordinates of points the walker visits as well as its
        starting and endposition
    """
    # create random locations
    walkers_locations = np.random.randint(
        low=0, high=number_of_steps, size=(number_of_steps, 2)
    )

    # split coordinates
    x_coord = walkers_locations[:, 0]
    y_coord = walkers_locations[:, 1]

    # calculate new coordinates for each step
    for step_number in range(1, number_of_steps):
        direction_of_step = np.random.randint(1, 5)
        if direction_of_step == 1:  # east
            x_coord[step_number] = x_coord[step_number - 1] + 1
            y_coord[step_number] = y_coord[step_number - 1]
        elif direction_of_step == 2:  # west
            x_coord[step_number] = x_coord[step_number - 1] - 1
            y_coord[step_number] = y_coord[step_number - 1]
        elif direction_of_step == 3:  # north
            x_coord[step_number] = x_coord[step_number - 1]
            y_coord[step_number] = y_coord[step_number - 1] + 1
        else:  # south
            x_coord[step_number] = x_coord[step_number - 1]
            y_coord[step_number] = y_coord[step_number - 1] - 1

    # return all coordinates and positions of the path
    return x_coord, y_coord


def plot_the_paths(list_of_walkers: list, outputfilename: str) -> None:
    """
    Creates the plots of the calculated paths of the walkers
    :param list_of_walkers: A list holding the walkers objects. Each object holds the
        coordinates of the respective path the walker walked.
    :param outputfilename: The file which will be created with the plotted paths
    """
    # define the number of rows and columns of subplots
    if len(list_of_walkers) == 1:
        columns_of_plots = 1
    else:
        columns_of_plots = 2
    rows_of_plots = math.ceil(len(list_of_walkers) / 2)

    # create the subplots
    figure, axis = plt.subplots(rows_of_plots, columns_of_plots, squeeze=False)
    for walker in enumerate(list_of_walkers):
        # get the walkers subplot and plot the path in it
        row = int(walker[0] / 2)
        if walker[0] % 2 == 0:
            column = 0
        else:
            column = 1
        if walker[1].walking_speed == 1:
            walker_type = "usual"
        elif walker[1].walking_speed == 2:
            walker_type = "fast"
        elif walker[1].walking_speed == 4:
            walker_type = "running"
        start_coordinates = walker[1].get_start_point()
        end_coordinates = walker[1].get_end_point()
        start_array = np.array(start_coordinates)
        end_array = np.array(end_coordinates)
        distance = start_array - end_array
        if np.absolute(distance[0]) and np.absolute(distance[1]) >= 50:
            axis[row, column].plot(
                [start_coordinates[0], end_coordinates[0]],
                [start_coordinates[1], end_coordinates[1]],
            )
            axis[row, column].set_title(
                f"Walker {walker[0] + 1} took a plane, "
                f"because the distance was too long"
            )
        else:
            axis[row, column].plot(walker[1].x_coordinates, walker[1].y_coordinates)
            axis[row, column].set_title(f"Walker {walker[0] + 1} is {walker_type}")
        axis[row, column].scatter(
            walker[1].get_start_point()[0],
            walker[1].get_start_point()[1],
            label="Startposition",
        )
        axis[row, column].scatter(
            walker[1].get_end_point()[0],
            walker[1].get_end_point()[1],
            label="Endposition",
        )
        axis[row, column].legend()

    if len(list_of_walkers) % 2 != 0 and len(list_of_walkers) != 1:
        # if the number of walkers is odd, delete the last (unused) subplot
        figure.delaxes(axis[(rows_of_plots - 1), 1])

    # arange subplot to not interfere each other, save the figure to the outputfile and
    # show the plot to the user
    figure.tight_layout()
    plt.savefig(outputfilename)
    plt.show()


class UsualWalker:
    """Represents a walker at usual speed"""

    def __init__(self, walking_time: int):
        self.walking_speed = 1
        self.walking_time = walking_time
        (
            self.x_coordinates,
            self.y_coordinates,
        ) = calculate_the_path(self.walking_time * self.walking_speed)

    def get_start_point(self) -> list:
        """
        gets the starting position of the walker
        :return: a list with the x-coordinate as the first element and the y-coordinate
            as the second element
        """
        return [self.x_coordinates[0], self.y_coordinates[0]]

    def get_end_point(self) -> list:
        """
        gets the last position of the walker
        :return: a list with the x-coordinate as the first element and the y-coordinate
            as the second element
        """
        return [self.x_coordinates[-1], self.y_coordinates[-1]]


class FastWalker:
    """Represents a walker at fast speed"""

    def __init__(self, walking_time: int):
        self.walking_speed = 2
        self.walking_time = walking_time
        (
            self.x_coordinates,
            self.y_coordinates,
        ) = calculate_the_path(self.walking_time * self.walking_speed)

    def get_start_point(self) -> list:
        """
        gets the starting position of the walker
        :return: a list with the x-coordinate as the first element and the y-coordinate
            as the second element
        """
        return [self.x_coordinates[0], self.y_coordinates[0]]

    def get_end_point(self) -> list:
        """
        gets the last position of the walker
        :return: a list with the x-coordinate as the first element and the y-coordinate
            as the second element
        """
        return [self.x_coordinates[-1], self.y_coordinates[-1]]


class RunningWalker:
    """Represents a walker at slow speed"""

    def __init__(self, walking_time: int):
        self.walking_speed = 4
        self.walking_time = walking_time
        (
            self.x_coordinates,
            self.y_coordinates,
        ) = calculate_the_path(self.walking_time * self.walking_speed)

    def get_start_point(self) -> list:
        """
        gets the starting position of the walker
        :return: a list with the x-coordinate as the first element and the y-coordinate
            as the second element
        """
        return [self.x_coordinates[0], self.y_coordinates[0]]

    def get_end_point(self) -> list:
        """
        gets the last position of the walker
        :return: a list with the x-coordinate as the first element and the y-coordinate
            as the second element
        """
        return [self.x_coordinates[-1], self.y_coordinates[-1]]


def main():
    """The main program. Assigns the user definitions, creates the scene and plots it"""
    try:
        # read in specifications defined by the user
        """walking_time = int(sys.argv[1]) + 1
        number_of_usual_walkers = int(sys.argv[2])
        number_of_fast_walkers = int(sys.argv[3])
        outputfilename = sys.argv[4]"""

        walking_time = 10000 + 1
        number_of_usual_walkers = 2
        number_of_fast_walkers = 1
        number_of_running_walkers = 1
        outputfilename = r"D:\Desktop\test_walker.png"

        number_of_walkers = (
            number_of_usual_walkers + number_of_fast_walkers + number_of_running_walkers
        )

        assert (
            walking_time > 1
        ), "walking_time must be greater than '0'. " "You stated '{}'".format(
            walking_time - 1
        )
        assert (
            number_of_walkers > 0
        ), "number_of_walkers must be greater than '1'. " "You stated '{}'".format(
            number_of_walkers
        )
        assert (
            number_of_walkers <= 12
        ), "number_of_walkers must be max. '12'. " "You stated '{}'".format(
            number_of_walkers
        )
    except ValueError as err:
        """This needs to be revised"""
        print(
            "Error: one of the inputs was not correctly specified.\n"
            "The Input must be specified as 'python main.py number_of_steps "
            "number_of_walkers outputfilename'.\n"
            "Inputformats: number_of_steps --> Integer, number_of_walkers --> "
            "Integer, outputfilename --> string\n"
            "outputfilename: path_to_output/filename.png\n"
            "The number of walkers and the number of steps to be made must be "
            "positive & at least 1\n\n\n",
            err,
        )
        sys.exit(1)

    scene = create_walkers(
        walking_time,
        number_of_usual_walkers,
        number_of_fast_walkers,
        number_of_running_walkers,
    )
    plot_the_paths(scene, outputfilename)


if __name__ == "__main__":
    main()
