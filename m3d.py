'''
m3d.py
Module for controlling the M3D printer over a serial port
Uses gcode commands to control the printer
Author: Greg d'Eon
Date: May 2, 2016
'''

import serial
import time

'''
Some of the most important gcode commands:
G0 [Xnnn] [Ynnn] [Znnn] 
 - Move to position (x, y, z) 
 - example: G0 X12 Y10.5 Z-2
G4 Pnnn
 - Wait for P milliseconds
 - example: G4 P200 (wait for 0.2 s)
G90
 - Turn on absolute positioning (default)
 - Coordinates are relative to origin
G91
 - Turn on relative positioning
 - Coordinates are relative to current position
M0
 - Stop all actions
 
Potential improvements:
- The printer doesn't seem to recognize where the ends of the X, Y, and Z axes 
  are. G-code supports stop-finding (ex: G0 X10 Y20 S1 to check for endstops),
  but these don't have any affect on the M3D.
  
- After resetting the printer or running into an axis stop, the position of the 
  origin appears to change. There are G-code commands to reset the coordinate
  system (G92) but they don't appear to work on the M3D printer.
'''

# Module variables
serialPort = None		# The serial port we're using


# ------------------------------------------------------------------------------
# Setup functions 
# ------------------------------------------------------------------------------
def start(port):
	"""
	Attempts to set up the M3D printer.

	Args:
		port (string): the COM port to be used (ex: "COM4")
	Returns:
		true if the printer is set up; otherwise false
	"""
	
	baud = 115200
	if not connect(port, baud):
		print "Could not connect to printer."
		return False
		
	if not switchToFirmware():
		print "Could not switch to firmware mode."
		return False
	
	return True


def connect(port, baud):
	"""
	Opens a serial connection with the M3D printer.
	
	Args:
		port: the COM port to be used (ex: "COM4")
		baud: the baudrate to be used (ex: 115200)
	Returns:
		true if the serial port was successfully opened; otherwise false
	"""
	
	global serialPort
	
	# Try to connect to port
	try:
		serialPort = serial.Serial(port, baud)
	except serial.SerialException as ex:
		print "Port is unavailable"
		serialPort = None
		return False
	
	return True


def switchToFirmware():
	"""
	Attempts to switch the printer into firmware mode.
	
	Returns:
		true if the switch was successful; otherwise false
	"""
	
	global serialPort
	
	# Fail if the serial port isn't opened
	if serialPort == None:
		return False
		
	# Tell the printer to switch to firmware mode
	serialPort.write("Q")
	time.sleep(0.5)
	
	# Attempt to reconnect to the printer
	try:
		serialPort.close()
		time.sleep(0.5)
		serialPort.open()
	except serial.SerialException as ex:
		# Failed to reconnect
		return False
	
	# All is well!
	return True

	
def disconnect():
	"""
	Closes the serial connection.
	"""
	
	global serialPort
	
	if serialPort != None:
		serialPort.close()
		serialPort = None



# ------------------------------------------------------------------------------
# Movement functions 
# ------------------------------------------------------------------------------		
def move(x = 0, y = 0, z = 0):
	"""
	Moves the printer head to the position (x, y, z)
	
	Args:
		x, y, z (number): coordinates
	"""
	
	# Build the command string
	command = "G0 X" + str(x) + " Y" + str(y) + " Z" + str(z) + " S1"
	serialPort.write(command)

	
def stop():
	"""
	Performs an emergency stop
	"""
	
	# Stop
	serialPort.write("M0")
	
	
def wait(ms):
	"""
	Waits in place for a fixed amount of time
	
	Args:
		ms (integer): amount of time to wait, in milliseconds
	"""
	
	# Wait for some time
	command = "G4 P" + str(ms)
	serialPort.write(command)
	
	
def setAbsolute():
	"""
	Puts the printer head in absolute coordinate mode
	"""
	
	# Set up absolute mode
	serialPort.write("G90")
	
	
def setRelative():
	"""
	Puts the printer head in relative coordinate mode
	"""
	
	# Set up absolute mode
	serialPort.write("G91")
	