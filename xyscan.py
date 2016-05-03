'''
xyscan.py
Uses a DSA815 with a loop antenna probe attached to an M3D printer head
to scan for EM signals over the surface of the chip.

Author: Greg d'Eon
Date: May 3, 2016
'''

import math
from m3d import *
from time import sleep

import matplotlib.pyplot as plt
import numpy as np

def plotHeatmap(data, dx, x_max, dy, y_max):
	"""
	Plot a heatmap.
	
	Args:
		Data: a 2D list of the data to be plotted
		dx, dy: the physical distance between consecutive data points
		x_max, y_max: the maximum distance to any data point
	"""
	
	# Generate x and y lists
	y, x = np.mgrid[slice(0, y_max+dy, dy),
					slice(0, x_max+dx, dx)]
	
	# Plot heatmap
	plt.pcolor(x, y, data, cmap=plt.cm.hot)
	plt.axis([0, x_max, 0, y_max])
	plt.colorbar()
	plt.show()



# Scan boundaries, in mm
x_max = 10
y_max = 10
step = 2
x_steps = int(math.ceil(x_max / step))
y_steps = int(math.ceil(y_max / step))

# M3D controller
printer = M3D()
printer.start("COM4")
printer.setRelative()
printer.move(0, 0)	# Change me to move to bottom left of chip!

# 2D list for scan result data
scanData = [[0 for j in range(x_steps)] for i in range(y_steps)]

# Scan over the surface
for y in range (y_steps):
	for x in range (x_steps):
		# Scan here
		scanData[y][x] = (x-4)*x + y*y
		print "x = {0:d}; y = {1:d}".format(x, y)
		time.sleep(0.1)
"""
		# Move in x
		printer.move(step, 0)
		if x == x_steps-1:
			printer.move(-x_max, 0)
	
	# Move in y
	printer.move(0, step)
	if y == y_steps-1:
		printer.move(0, -y_max)
"""

		
print(scanData)

# Plot scan data
plotHeatmap(scanData, step, x_max, step, y_max)


