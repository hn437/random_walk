#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A Random Walk Simulation
"""

# Python code for 2D random walk.
import numpy
import matplotlib.pyplot as plt
import random

# defining the number of steps
n = 100000

# creating two array for containing x and y coordinate
# of size equals to the number of size and filled up with 0's
x = numpy.zeros(n)
y = numpy.zeros(n)

# filling the coordinates with random variables
for i in range(1, n):
    val = random.randint(1, 4)
    if val == 1:
        x[i] = x[i - 1] + 1
        y[i] = y[i - 1]
    elif val == 2:
        x[i] = x[i - 1] - 1
        y[i] = y[i - 1]
    elif val == 3:
        x[i] = x[i - 1]
        y[i] = y[i - 1] + 1
    else:
        x[i] = x[i - 1]
        y[i] = y[i - 1] - 1


# plotting the walk
plt.title("Random Walk ($n = " + str(n) + "$ steps)")
plt.plot(x, y)
plt.savefig("rand_walk"+str(n)+".png",bbox_inches="tight",dpi=600)
plt.show()