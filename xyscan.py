'''
xyscan.py
Uses a DSA815 with a loop antenna probe attached to an M3D printer head
to scan for EM signals over the surface of the chip.

Author: Greg d'Eon
Date: May 3-4, 2016
'''

# Controllers
from m3d import *
from dsa815 import *

# Utilities
import math
from time import sleep

# Plotting
import matplotlib.pyplot as plt
import numpy as np


def plotHeatmap(data, x_min, x_max, y_min, y_max, filename):
	"""
	Plot a heatmap.
	
	Args:
		Data: a 2D list of the data to be plotted
		x_min, y_min: the minimum coordinate of any data point
		x_max, y_max: the maximum coordinate any data point
		filename: where to save this image
	"""
	
	# Generate x and y lists
	x_points = numpy.linspace(x_min, x_max, len(data[0]))
	y_points = numpy.linspace(y_min, y_max, len(data))
	
	x, y = numpy.meshgrid(x_points, y_points)
	
	# Plot heatmap
	fig = plt.figure()
	plt.pcolor(x, y, data, cmap=plt.cm.Blues)
	plt.axis([x_min, x_max, y_min, y_max])
	plt.colorbar()
	plt.xlabel("Frequency / Hz")
	plt.ylabel("Y coordinate / mm")
	fig.savefig(filename, bbox_inches="tight")

	
# Main script
if __name__ == '__main__':

	# Scan layout
	x_step = 5		# Step size, in mm
	y_step = 2		# Step size, in mm
	x_steps = 2		# Number of steps to take
	y_steps = 5		# Number of steps to take
	
	x_max = x_step * x_steps	# Size of the grid we're measuring
	y_max = y_step * y_steps	# Note that we'll never reach x = x_max
	
	
	# M3D controller
	printer = M3D()
	printer.start("COM4")
	printer.setRelative()
	printer.move(0, 0, 0)	# Change me to move to bottom left of chip
	
	
	# Scan frequencies, in Hz
	f_low = 1e6
	f_hi  = 601e6
	RBW   = 30e3
	num_freqs = 601	# This seems to be fixed for the DSA815
	
	# DSA815 controller
	scope = DSA815()
	scope.conn("USB0::0x1AB1::0x0960::DSA8A134700016::INSTR")	
	scope.set_freq_limits(f_low, f_hi)
	scope.set_RBW(RBW)
	scope.enable_RF(True)
	scope.set_input_atten(0)
	
	
	# 3D list for scan result data
	# scanData[x][y][f] is data at position (x, y) and frequency f
	# (ie: one output from DSA is scanData[x][y])
	scanData = [[[0 for k in range(num_freqs+1)] 
				for j in range(y_steps)] 
				for i in range(x_steps)]
	
	# Scan over the surface
	for y in range (y_steps):
		for x in range (x_steps):
			# Wait for the head to stop moving
			time.sleep(0.1)
			
			# Scan with the spectrum analyzer
			scanData[x][y] = scope.measure_trace()
			
			# Note where we are
			print "x = {0:d}; y = {1:d}".format(x, y)
			time.sleep(0.1)
	
			# Move in x
			if x == x_steps-1:
				printer.move(x_step - x_max, 0)
			else:
				printer.move(x_step, 0)
			
				
		# Move in y
		if y == y_steps-1:
			printer.move(0, y_step - y_max)
		else:
			printer.move(0, y_step)
	
	printer.stop()
	
	
	# Plot scan data
	for i in range(len(scanData)):
		plotHeatmap(scanData[i], f_low, f_hi, 0, y_max - y_step, "image{}".format(i))
	
	
	