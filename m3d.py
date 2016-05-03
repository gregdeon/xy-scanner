'''
m3d.py
Module for controlling the M3D printer over a serial port
Uses gcode commands to control the printer
Author: Greg d'Eon
Date: May 2, 2016
'''

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

import serial
import time

class M3D(object):
	# Constructor/destructor
	def __init__(self):
		self.serialPort = None

	def dis(self):
		self.__disconnect()
		del self.serialPort
		
	# Setup functions
	def start(self, port):
		"""
		Attempts to set up the M3D printer.
	
		Args:
			port (string): the COM port to be used (ex: "COM4")
		Returns:
			true if the printer is set up; otherwise false
		"""
		
		baud = 115200
		if not self.__connect(port, baud):
			print "Could not connect to printer."
			return False
			
		if not self.__switchToFirmware():
			print "Could not switch to firmware mode."
			return False
		
		return True
	
	
	def __connect(self, port, baud):
		"""
		Opens a serial connection with the M3D printer.
		
		Args:
			port: the COM port to be used (ex: "COM4")
			baud: the baudrate to be used (ex: 115200)
		Returns:
			true if the serial port was successfully opened; otherwise false
		"""
		
		# Try to connect to port
		try:
			self.serialPort = serial.Serial(port, baud)
		except serial.SerialException as ex:
			print "Port is unavailable"
			self.serialPort = None
			return False
		
		return True
	
	
	def __switchToFirmware(self):
		"""
		Attempts to switch the printer into firmware mode.
		
		Returns:
			true if the switch was successful; otherwise false
		"""
		
		# Fail if the serial port isn't opened
		if self.serialPort == None:
			return False
			
		# Tell the printer to switch to firmware mode
		self.serialPort.write("Q")
		time.sleep(0.5)
		
		# Attempt to reconnect to the printer
		try:
			self.serialPort.close()
			time.sleep(0.5)
			self.serialPort.open()
		except serial.SerialException as ex:
			# Failed to reconnect
			return False
		
		# All is well!
		return True
	
		
	def __disconnect(self):
		"""
		Closes the serial connection.
		"""
		
		if self.serialPort != None:
			self.serialPort.close()
			self.serialPort = None
	
	
	
	# Movement functions 	
	def move(self, x = 0, y = 0, z = 0):
		"""
		Moves the printer head to the position (x, y, z)
		
		Args:
			x, y, z (number): coordinates
		"""
		
		# Build the command string
		command = "G0 X" + str(x) + " Y" + str(y) + " Z" + str(z) + " S1"
		self.serialPort.write(command)
	
		
	def stop(self):
		"""
		Performs an emergency stop
		"""
		
		# Stop
		self.serialPort.write("M0")
		
		
	def wait(self, ms):
		"""
		Waits in place for a fixed amount of time
		
		Args:
			ms (integer): amount of time to wait, in milliseconds
		"""
		
		# Wait for some time
		command = "G4 P" + str(ms)
		self.serialPort.write(command)
		
		
	def setAbsolute(self):
		"""
		Puts the printer head in absolute coordinate mode
		"""
		
		# Set up absolute mode
		self.serialPort.write("G90")
		
		
	def setRelative(self):
		"""
		Puts the printer head in relative coordinate mode
		"""
		
		# Set up absolute mode
		self.serialPort.write("G91")
	

"""
Example code to control the printer
"""
if __name__ == '__main__':
	test = M3D()
	
	print "Setting up..."
	test.start("COM4")
	
	print "Testing movement..."
	test.setRelative()
	test.move( 10,  10, 0)
	test.move(-10,   0, 0)
	test.move(  0,  10, 0)
	test.wait(500)
	test.move(  0,  -20, 1)
	
	print "Tearing down..."
	# Happens automatically
	