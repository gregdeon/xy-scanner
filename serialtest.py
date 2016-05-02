import serial

# Open serial port COM4
ser = serial.Serial(3)

# Check that we've opened COM4
print "Opened serial port " + ser.portstr

# Open a file with several gcode commands
fin = open("gcode.txt", "r")

# Write them to the printer one at a time
for line in fin:
	print ">> " + line
	ser.write(line)

# Pack up and go home
fin.close()
ser.close()