#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contains tests for the walker class"""

import os
import tempfile

import numpy as np
import pytest
from matplotlib.image import imread

import walker


def test_scene_creation_successful():
    """Tests whether a scene is created according to the user input. As the path is
    calculated while creating the scene, it also checks that no error message is
    thrown while calculating it, however, it does not test if the calculation
    function calculates the way it is supposed to"""
    # define three walker
    walking_time = 10
    number_of_usual_walker = 1
    number_of_fast_walker = 1
    number_of_running_walker = 1
    # create scene
    scene = walker.create_walker(
        walking_time,
        number_of_usual_walker,
        number_of_fast_walker,
        number_of_running_walker,
    )
    # check if result has the expected length
    assert len(scene) == 3


def test_scene_creation_invalid_input_no_walker():
    """Tests whether the validation check of the user input works and stops the
    calculation due to invalid inputs"""
    with pytest.raises(AssertionError):  # error zero walker
        walker.create_walker(
            walking_time=1,
            number_of_usual_walker=0,
            number_of_fast_walker=0,
            number_of_running_walker=0,
        )


def test_scene_creation_invalid_input_negative_number_of_walker():
    """Tests whether the validation check of the user input works and stops the
    calculation due to invalid inputs"""
    with pytest.raises(AssertionError):  # error negative number of walker
        walker.create_walker(
            walking_time=1,
            number_of_usual_walker=1,
            number_of_fast_walker=1,
            number_of_running_walker=-1,
        )
    with pytest.raises(AssertionError):  # error negative number of walker
        walker.create_walker(
            walking_time=1,
            number_of_usual_walker=1,
            number_of_fast_walker=-1,
            number_of_running_walker=1,
        )
    with pytest.raises(AssertionError):  # error negative number of walker
        walker.create_walker(
            walking_time=1,
            number_of_usual_walker=-1,
            number_of_fast_walker=1,
            number_of_running_walker=1,
        )


def test_scene_creation_invalid_input_too_many_walker():
    """Tests whether the validation check of the user input works and stops the
    calculation due to invalid inputs"""
    with pytest.raises(AssertionError):  # error more than 12 walker
        walker.create_walker(
            walking_time=1,
            number_of_usual_walker=10,
            number_of_fast_walker=2,
            number_of_running_walker=2,
        )


def test_usual_walker_coordinate_length():
    """Tests whether the correct amount of coordinates is created for the usual
    walker"""
    walking_time = 2
    walking_speed = 1
    # walker does one steps in 1 time, and has two times. plus needs a starting
    #   coordinate
    expected_len_coordinates = 1 + 1 + 1
    usual_walker = walker.Walker(walking_time, walking_speed)
    assert len(usual_walker.x_coordinates) == expected_len_coordinates
    assert len(usual_walker.y_coordinates) == expected_len_coordinates


def test_fast_walker_coordinate_length():
    """Tests whether the correct amount of coordinates is created for the fast walker"""
    walking_time = 2
    walking_speed = 2
    # walker does two steps in 1 time, and has two times. plus needs a starting
    #   coordinate
    expected_len_coordinates = 2 + 2 + 1
    fast_walker = walker.Walker(walking_time, walking_speed)
    assert len(fast_walker.x_coordinates) == expected_len_coordinates
    assert len(fast_walker.y_coordinates) == expected_len_coordinates


def test_running_walker_coordinate_length():
    """Tests whether the correct amount of coordinates is created for the running
    walker"""
    walking_time = 2
    walking_speed = 4
    # walker does four steps in 1 time, and has two times. plus needs a starting
    #   coordinate
    expected_len_coordinates = 4 + 4 + 1
    running_walker = walker.Walker(walking_time, walking_speed)
    assert len(running_walker.x_coordinates) == expected_len_coordinates
    assert len(running_walker.y_coordinates) == expected_len_coordinates


def test_path_calculation():
    """tests whether the path calculation works correctly by checking if each coordinate
    varies from the coordinate before by max. 1"""
    walking_time = 2
    walking_speed = 4
    running_walker = walker.Walker(walking_time, walking_speed)
    running_walker.calculate_the_path()

    # prepare check for total coordinate variation
    expected_total_difference = 4 + 4
    total_difference = 0

    for i in range(1, len(running_walker.x_coordinates)):
        x_difference = abs(
            running_walker.x_coordinates[i] - running_walker.x_coordinates[i - 1]
        )
        y_difference = abs(
            running_walker.y_coordinates[i] - running_walker.y_coordinates[i - 1]
        )
        total_difference += x_difference + y_difference
        assert x_difference in (0, 1)
        assert y_difference in (0, 1)

    assert total_difference == expected_total_difference


def test_calculate_next_step():
    """Tests whether all directions can be chosen by the walker. Calculates the next
    step 100 times and check in which direction it was taken. Afterwards it is
    checked that each direction was chosen at least once"""
    walking_time = 1
    walking_speed = 1
    counter_east = counter_west = counter_north = counter_south = 0
    test_walker = walker.Walker(walking_time, walking_speed)
    for _ in range(100):
        test_walker.x_coordinates = np.array([1, 1])
        test_walker.y_coordinates = np.array([1, 1])
        test_walker.calculate_next_step(1)
        if test_walker.x_coordinates[1] == 2:
            counter_east += 1
        elif test_walker.x_coordinates[1] == 0:
            counter_west += 1
        elif test_walker.y_coordinates[1] == 2:
            counter_north += 1
        elif test_walker.y_coordinates[1] == 0:
            counter_south += 1
    assert (
        counter_north > 0
        and counter_south > 0
        and counter_west > 0
        and counter_east > 0
    )


def test_create_building():
    """Tests whether the building is created correctly. The starting coordinates are set
    manually as well as the expected building. The actual building is calculated
    with the walker function and compared to the expected"""
    expected_building = [-20.5, 19.5, 0.5, 15.5]
    walking_time = 1
    walking_speed = 1
    test_walker = walker.Walker(walking_time, walking_speed)
    test_walker.x_coordinates = np.array([0, 0])
    test_walker.y_coordinates = np.array([0, 0])
    actual_building = test_walker.create_building()
    assert actual_building == expected_building


def test_avoid_building():
    """tests whether the walker avoids the building.

    Testing mode: as the building is avoided using a while loop, the test is not
    that simple using a real walker. Instead, the coordinates of the walker are set
    and the building is set to be reached by the walker if he does a step eastwards
    (x-coordinate +1). Then, the path-calculation is executed. The resulting
    coordinate is checked, it must be outside the building. However, the chance of
    the walker walking in the direction of the building is only 25%. Therefore, the
    check is done 100 times, so hypothetical the walker tries to walk into the
    building 25 times"""
    walking_time = 1
    walking_speed = 1
    test_walker = walker.Walker(walking_time, walking_speed)
    for _ in range(100):
        test_walker.x_coordinates = np.array([1, 1])
        test_walker.y_coordinates = np.array([1, 1])
        test_walker.building = [1.5, 10.5, -20, 20]
        test_walker.calculate_the_path()
        assert test_walker.x_coordinates[1] != 2


def test_get_start_point():
    """Test whether the correct coordinates are returned for the start point"""
    walking_time = 1
    walking_speed = 1
    test_walker = walker.Walker(walking_time, walking_speed)
    test_walker.x_coordinates = np.array([0, 1])
    test_walker.y_coordinates = np.array([9, 10])
    assert [0, 9] == test_walker.get_start_point()


def test_get_end_point():
    """Test whether the correct coordinates are returned for the end point"""
    walking_time = 1
    walking_speed = 1
    test_walker = walker.Walker(walking_time, walking_speed)
    test_walker.x_coordinates = np.array([0, 1])
    test_walker.y_coordinates = np.array([9, 10])
    assert [1, 10] == test_walker.get_end_point()


def test_plotting():
    """Test that an image is written by the function plot_the_paths() and that it can
    be opened"""
    walking_time = 1
    walking_speed = 1
    outfile_name = "test_image.png"
    test_walker = walker.Walker(walking_time, walking_speed)
    test_walker.calculate_the_path()
    with tempfile.TemporaryDirectory() as tmp_dirname:
        outfile = os.path.join(tmp_dirname, outfile_name)
        walker.plot_the_paths([test_walker], outfile)
        image = imread(outfile)
        assert len(image.shape) == 3
