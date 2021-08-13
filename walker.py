#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A Random Walk Simulation For Multiple Walker"""
# based on the idea of:
# Python code for 2D random walk.
# Source: https://www.geeksforgeeks.org/random-walk-implementation-python/

import math
import sys

import matplotlib.pyplot as plt
import numpy as np


def create_walker(
    walking_time: int,
    number_of_usual_walker: int,
    number_of_fast_walker: int,
    number_of_running_walker: int,
) -> list:
    """
    Checks if all user definitions of the walker are valid. If so, Creates a list of
        all walker objects and calculates their paths.
    :param walking_time: the 'time' each walker walks and therefore (depending on it's
        respective speed) the number of steps the walker will make
    :param number_of_usual_walker: the number of usual walker defines the number of
        objects of this respective class which will be appended to the scene
    :param number_of_fast_walker:the number of fast walker defines the number of
        objects of this respective class which will be appended to the scene
    :param number_of_running_walker: the number of running walker defines the number
        of objects of this respective class which will be appended to the scene
    :return: a list, the 'scene' which contains all walker, so all objects and their
        coordinates
    """
    number_of_walker = (
        number_of_usual_walker + number_of_fast_walker + number_of_running_walker
    )
    assert (
        walking_time >= 1
    ), "walking_time must be greater than '0'. " "You stated '{}'".format(
        walking_time - 1
    )
    assert (
        number_of_usual_walker >= 0
        and number_of_fast_walker >= 0
        and number_of_running_walker >= 0
    ), (
        "The number of walker can't be negative for any class. You stated '{}', "
        "'{}' and '{}' for the walker classes".format(
            number_of_usual_walker, number_of_fast_walker, number_of_running_walker
        )
    )
    assert (
        number_of_walker > 0
    ), "The number of walker must be greater than '1'. " "You stated {}".format(
        number_of_walker
    )
    assert (
        number_of_walker <= 12
    ), "The number of walker must be max. '12'. " "You stated {}".format(
        number_of_walker
    )

    scene = []
    for _ in range(number_of_usual_walker):
        # create the array of a walker and add it to the scene-list
        scene.append(Walker(walking_time, 1))
    for _ in range(number_of_fast_walker):
        # create the array of a walker and add it to the scene-list
        scene.append(Walker(walking_time, 2))
    for _ in range(number_of_running_walker):
        # create the array of a running walker and add it to the scene-list
        scene.append(Walker(walking_time, 4))
    for walker in scene:
        walker.calculate_the_path()
        continue
    return scene


def plot_the_paths(list_of_walker: list, outfile_name: str) -> None:
    """
    Creates the plots of the calculated paths of the walker as well as the building
        next to it
    :param list_of_walker: A list holding the walker objects. Each object holds the
        coordinates of the respective path the walker walked.
    :param outfile_name: The file which will be created with the plotted paths
    """
    # define the number of rows and columns of subplots
    if len(list_of_walker) == 1:
        columns_of_plots = 1
    else:
        columns_of_plots = 2
    rows_of_plots = math.ceil(len(list_of_walker) / 2)

    # create the subplots
    figure, axes = plt.subplots(rows_of_plots, columns_of_plots, squeeze=False)
    figure.set_figheight(4.8 * rows_of_plots + 1)
    flying_walker = []
    for walker in enumerate(list_of_walker):
        # get the walker subplot and plot the path in it
        row = int(walker[0] / 2)
        if walker[0] % 2 == 0:
            column = 0
        else:
            column = 1
        if walker[1].walking_speed == 1:
            walker_type = "walking casually"
        elif walker[1].walking_speed == 2:
            walker_type = "walking fast"
        elif walker[1].walking_speed == 4:
            walker_type = "running"
        start_coordinates = np.array(walker[1].get_start_point())
        end_coordinates = np.array(walker[1].get_end_point())
        distance = start_coordinates - end_coordinates
        if (
            math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        ) >= 150:  # pythagorean theorem
            axes[row, column].plot(
                [start_coordinates[0], end_coordinates[0]],
                [start_coordinates[1], end_coordinates[1]],
            )
            flying_walker.append(walker[0] + 1)
        else:
            axes[row, column].plot(walker[1].x_coordinates, walker[1].y_coordinates)
        axes[row, column].fill(
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
            c="grey",
            label="Building",
        )
        axes[row, column].scatter(
            walker[1].get_start_point()[0],
            walker[1].get_start_point()[1],
            label="Startposition",
            marker="o",
            c="turquoise",
        )
        axes[row, column].scatter(
            walker[1].get_end_point()[0],
            walker[1].get_end_point()[1],
            label="Endposition",
            marker="^",
            c="orange",
        )
        axes[row, column].legend()
        axes[row, column].set_title(f"Walker {walker[0] + 1} is {walker_type}")

    if len(list_of_walker) % 2 != 0 and len(list_of_walker) != 1:
        # if the number of walker is odd, delete the last (unused) subplot
        figure.delaxes(axes[(rows_of_plots - 1), 1])

    # arrange subplot to not interfere each other, save the figure to the outfile and
    # show the plot to the user
    if len(flying_walker) > 0:
        plt.figtext(
            0.5,
            0.01,
            f"\nWalker(s) {flying_walker} took a plane, as they don't want to walk"
            f"such a long distance!",
            ha="center",
        )
    figure.tight_layout(rect=[0, 0.01, 1, 1])
    plt.savefig(outfile_name)
    plt.show()


class Walker:
    """Represents a walker to which a walking speed and walking time are given"""

    def __init__(self, walking_time: int, walking_speed: int):
        self.walking_speed = walking_speed
        self.walking_time = walking_time
        self.number_of_steps = self.walking_time * self.walking_speed + 1
        (self.x_coordinates, self.y_coordinates) = self.assign_random_coordinates()
        self.building = self.create_building()

    def assign_random_coordinates(self) -> tuple:
        """
        This function creates random coordinates, as many as the walker does steps.
            These will be updated later when the walker walks by calling the function
            calculate_the_path()
        :return: A tuple of two arrays holding the x- or y-coordinates
        """
        # create random coordinates
        x_coord = np.random.randint(
            low=0, high=self.number_of_steps, size=self.number_of_steps
        )
        y_coord = np.random.randint(
            low=0, high=self.number_of_steps, size=self.number_of_steps
        )
        return x_coord, y_coord

    def calculate_the_path(self) -> None:
        """
        Calculates the path the walker walks by updating each position and checking if
        the walker does not collide with the building.
        """
        # calculate new coordinates for each step
        for step_number in range(1, self.number_of_steps):
            self.calculate_next_step(step_number)
            while (
                (self.x_coordinates[step_number] > self.building[0])
                and (self.x_coordinates[step_number] < self.building[1])
                and (self.y_coordinates[step_number] > self.building[2])
                and (self.y_coordinates[step_number] < self.building[3])
            ):
                self.calculate_next_step(step_number)

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

    def calculate_next_step(self, step_number: int) -> None:
        """
        This is a helper function which is used by the function calculate_the_path. It
            is executed each time the next step needs to be calculated or if the walker
            would walk into the building. It takes a random direction and updates the
            coordinates from the position before and adds a step according to the
            randomly determined direction
        :param step_number: The number of step to be calculated
        """
        direction_of_step = np.random.randint(1, 5)
        if direction_of_step == 1:  # east
            self.x_coordinates[step_number] = self.x_coordinates[step_number - 1] + 1
            self.y_coordinates[step_number] = self.y_coordinates[step_number - 1]
        elif direction_of_step == 2:  # west
            self.x_coordinates[step_number] = self.x_coordinates[step_number - 1] - 1
            self.y_coordinates[step_number] = self.y_coordinates[step_number - 1]
        elif direction_of_step == 3:  # north
            self.x_coordinates[step_number] = self.x_coordinates[step_number - 1]
            self.y_coordinates[step_number] = self.y_coordinates[step_number - 1] + 1
        else:  # south
            self.x_coordinates[step_number] = self.x_coordinates[step_number - 1]
            self.y_coordinates[step_number] = self.y_coordinates[step_number - 1] - 1

    def create_building(self) -> list:
        """
        This function calculates the building of the walker. It's a rectangle north of
            the walker starting position
        :return: a list holding the 4 coordinates of the building
        """
        xmin = float(self.get_start_point()[0]) - 20.5
        xmax = xmin + 40
        ymin = float(self.get_start_point()[1]) + 0.5
        ymax = ymin + 15
        return [xmin, xmax, ymin, ymax]


def main():
    """The main program. Assigns the user definitions, creates the scene and plots it"""
    # read in specifications defined by the user
    try:
        walking_time = int(sys.argv[1])
        number_of_usual_walker = int(sys.argv[2])
        number_of_fast_walker = int(sys.argv[3])
        number_of_running_walker = int(sys.argv[4])
        outfile_name = sys.argv[5]
    except (SyntaxError, IndexError, ValueError) as err:
        print(
            "Error: At least one of the inputs was not correctly specified.\n"
            "The Input must be specified as 'python walker.py walking_time "
            "number_of_usual_walker number_of_fast_walker number_of_running_walker "
            "outfile_name'.\n"
            "Inputformats: walking time --> Integer, number of walker --> "
            "Integer, outfile_name --> string\n"
            "outfile_name: path_to_output/filename.png\n"
            "The number of walker and the walking time must be positive & at least 1"
            "\n\n\n",
            err,
        )
        sys.exit(1)

    scene = create_walker(
        walking_time,
        number_of_usual_walker,
        number_of_fast_walker,
        number_of_running_walker,
    )
    plot_the_paths(scene, outfile_name)


if __name__ == "__main__":
    main()
