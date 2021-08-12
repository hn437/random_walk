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
        scene.append(Walker(walking_time, 1))
    for _ in range(number_of_fast_walkers):
        # create the array of a walker and add it to the scene-list
        scene.append(Walker(walking_time, 2))
    for _ in range(number_of_running_walkers):
        # create the array of a running walker and add it to the scene-list
        scene.append(Walker(walking_time, 4))
    return scene


def create_building(
    walker_x_startcoordinate: np.ndarray,
    walker_y_startcoordinate: np.ndarray,
    number_of_steps: int,
) -> list:
    """

    :param walker_x_startcoordinate:
    :param walker_y_startcoordinate:
    :return:
    """
    xmin = (
        float(walker_x_startcoordinate)
        + float(math.ceil(number_of_steps / number_of_steps * 1.1))
        + 0.5
    )
    xmax = xmin + 30
    ymin = (
        float(walker_y_startcoordinate)
        + float(math.ceil(number_of_steps / number_of_steps * 1.1))
        + 0.5
    )
    ymax = ymin + 10
    return [xmin, xmax, ymin, ymax]


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
    figure, axes = plt.subplots(rows_of_plots, columns_of_plots, squeeze=False)
    figure.set_figheight(4.8 * rows_of_plots + 1)
    flying_walkers = []
    for walker in enumerate(list_of_walkers):
        # get the walkers subplot and plot the path in it
        row = int(walker[0] / 2)
        if walker[0] % 2 == 0:
            column = 0
        else:
            column = 1
        if walker[1].walking_speed == 1:
            walker_type = "walking at usual speed"
        elif walker[1].walking_speed == 2:
            walker_type = "walking fast"
        elif walker[1].walking_speed == 4:
            walker_type = "running"
        start_coordinates = np.array(walker[1].get_start_point())
        end_coordinates = np.array(walker[1].get_end_point())
        distance = start_coordinates - end_coordinates
        if (
            math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        ) >= 100:  # pythagorean theorem
            axes[row, column].plot(
                [start_coordinates[0], end_coordinates[0]],
                [start_coordinates[1], end_coordinates[1]],
            )
            flying_walkers.append(walker[0] + 1)
        else:
            axes[row, column].plot(walker[1].x_coordinates, walker[1].y_coordinates)
        axes[row, column].plot(
            [
                walker[1].building[0],
                walker[1].building[1],
                walker[1].building[1],
                walker[1].building[0],
                walker[1].building[0],
            ],
            [
                walker[1].building[2],
                walker[1].building[2],
                walker[1].building[3],
                walker[1].building[3],
                walker[1].building[2],
            ],
            c="black",
        )
        axes[row, column].scatter(
            walker[1].get_start_point()[0],
            walker[1].get_start_point()[1],
            label="Startposition",
            marker="o",
        )
        axes[row, column].scatter(
            walker[1].get_end_point()[0],
            walker[1].get_end_point()[1],
            label="Endposition",
            marker="^",
        )
        axes[row, column].legend()
        axes[row, column].set_title(f"Walker {walker[0] + 1} is {walker_type}")

    if len(list_of_walkers) % 2 != 0 and len(list_of_walkers) != 1:
        # if the number of walkers is odd, delete the last (unused) subplot
        figure.delaxes(axes[(rows_of_plots - 1), 1])

    # arange subplot to not interfere each other, save the figure to the outputfile and
    # show the plot to the user
    if len(flying_walkers) > 0:
        plt.figtext(
            0.5,
            0.01,
            f"\nWalker(s) {flying_walkers} took a plane, as they don't walk such a long distance!",
            ha="center",
        )
    figure.tight_layout(rect=[0, 0.01, 1, 1])
    plt.savefig(outputfilename)
    plt.show()


class Walker:
    """Represents a walker which is given a walking speed and walking time to"""

    def __init__(self, walking_time: int, walking_speed: int):
        self.walking_speed = walking_speed
        self.walking_time = walking_time
        (self.x_coordinates, self.y_coordinates, self.building) = self.calculate_the_path()

    def calculate_the_path(self) -> tuple:
        """
        Calculates the path the walker walks
        :param number_of_steps: the number of steps the walker takes
        :return: all x- and all y- coordinates of points the walker visits as well as its
            starting and endposition
        """
        # calculate the number of steps
        number_of_steps = self.walking_time * self.walking_speed + 1
        # create random coordinates
        x_coord = np.random.randint(low=0, high=number_of_steps, size=number_of_steps)
        y_coord = np.random.randint(low=0, high=number_of_steps, size=number_of_steps)

        # initiate building
        building = create_building(x_coord[0], y_coord[0], number_of_steps)

        # calculate new coordinates for each step
        for step_number in range(1, number_of_steps):
            x_coord, y_coord = self.calculate_next_step(step_number, x_coord, y_coord)
            while (
                    (x_coord[step_number] > building[0])
                    and (x_coord[step_number] < building[1])
                    and (y_coord[step_number] > building[2])
                    and (y_coord[step_number] < building[3])
            ):
                x_coord, y_coord = self.calculate_next_step(step_number, x_coord, y_coord)

        # return all coordinates and positions of the path
        return x_coord, y_coord, building

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

    def calculate_next_step(self, step_number: int, x_coord: np.ndarray, y_coord: np.ndarray):
        """
        This is a helper function which is used by the function calculate_the_path. It
            is executed each time the next step needs to be calculated or if the walker
            would walk into the building
        :param step_number: The number of step to be calculated
        :param x_coord: the array of x-coordinates, of which the one at position
            step_number will be calculated
        :param y_coord: the array of y-coordinates, of which the one at position
            step_number will be calculated
        :return: the updated coordinate arrays
        """
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
        return x_coord, y_coord


def main():
    """The main program. Assigns the user definitions, creates the scene and plots it"""
    try:
        # read in specifications defined by the user
        """walking_time = int(sys.argv[1])
        number_of_usual_walkers = int(sys.argv[2])
        number_of_fast_walkers = int(sys.argv[3])
        number_of_running_walkers = int(sys.argv[4])
        outputfilename = sys.argv[5]"""

        walking_time = 100
        number_of_usual_walkers = 2
        number_of_fast_walkers = 1
        number_of_running_walkers = 1
        outputfilename = r"D:\Desktop\test_walker.png"

        number_of_walkers = (
            number_of_usual_walkers + number_of_fast_walkers + number_of_running_walkers
        )

        assert (
            walking_time >= 1
        ), "walking_time must be greater than '0'. " "You stated '{}'".format(
            walking_time - 1
        )
        assert (
            number_of_usual_walkers >= 0
            and number_of_fast_walkers >= 0
            and number_of_running_walkers
        ), "The number of walkers can't be negative for any class. You stated '{}', '{}'and '{}' for the walker classes".format(
            number_of_usual_walkers, number_of_fast_walkers, number_of_running_walkers
        )
        assert (
            number_of_walkers > 0
        ), "The number of walkers must be greater than '1'. " "You stated {}".format(
            number_of_walkers
        )
        assert (
            number_of_walkers <= 12
        ), "The number of walkers must be max. '12'. " "You stated {}".format(
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
