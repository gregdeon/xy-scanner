'''
m3dtest.py
Testing program for m3d.py
'''

import m3d

# Set up
if m3d.start("COM4"):
	# Move around
	m3d.setAbsolute()
	m3d.move(40, 40, 0)
	m3d.wait(1000)
	m3d.setRelative()
	m3d.move(-10, -10, 0)
	m3d.move( 10,   0, 0)
	m3d.move(  0,  -10, 0)
	
	# Tear down
	m3d.disconnect()
