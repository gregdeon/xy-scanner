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

# Scan over a rectangle
# Scan boundaries
x_max = 10
y_max = 10
step = 5

x_steps = int(math.ceil(x_max / step))
y_steps = int(math.ceil(y_max / step))

# M3D controller
printer = M3D()
printer.start("COM4")
printer.setRelative()

printer.move(0, 0)

for y in range (y_steps+1):
	for x in range (x_steps+1):
		# Scan here
		print "x = {0:d}; y = {1:d}".format(x, y)
		time.sleep(0.1)
		
		# Move in x
		if x == x_steps:
			printer.move(-x_max, 0)
		else:
			printer.move(step, 0)
	
	# Move in y
	if y == y_steps:
		printer.move(0, -y_max)
	else:
		printer.move(0, step)

		
