'''
dsa815.py
Controls a DSA815 spectrum analyzer.
Adapted from Colin O'Flynn's DSA815 module (github.com/colinoflynn/dsa815)

Author: Greg d'Eon
Date: May 3-4, 2016
'''

import numpy
import visa
import time

class DSA815(object):
	# Setup and teardown
	def __init__(self):
		pass

		
	def conn(self, constr="USB0::0x1AB1::0x0960::DSA8Axxxxxxx::INSTR"):
		"""
		Attempt to connect to instrument
		
		Args:
			constr (string): the location of the spectrum analyzer
		"""
		
		rm = visa.ResourceManager()
		self.inst = rm.open_resource(constr)
	

	def dis(self):
		del self.inst
	

	def identify(self):
		"""
		Return identify string, which has serial number
		
		Returns:
			(string) Identity of the instrument
			ex: Rigol Technologies,DSA815,DSA8A134700016,00.01.12.00.02
 		"""
		
		return self.inst.ask("*IDN?")

	
	# Settings
	def TG_enable(self, state):
		"""
		Turn the tracking generator on or off.
		
		Args:
			state (True/False): true if the tracking generator will be turned on
		"""
		
		if state:
			tstate = "1"
		else:
			tstate = "0"

		self.inst.write(":OUTput:STATe %s\n"%tstate)
		

	def TG_amp(self, amp):
		"""
		Set the TG output amplitude power in dBm
		
		Args:
			amp (number): the output power, from -20 dBm to 0 dBm.
			
		Raises:
			ValueError: if the amplitude is outside of the range [-20, 0]
		"""

		if amp > 0 or amp < -20:
			raise ValueError("Amplitude outside of allowed range -20dBm to 0dBm")
		
		self.inst.write(":SOUR:POW:LEV:IMM:AMPL %d\n"%amp)

	def set_freq_limits(self, f_low, f_hi):
		"""
		Set the frequency range on the spectrum analyzer.
		
		Args:
			f_low: The minimum frequency to scan
			f_hi: The maximum frequency
		
		Raises:
			ValueError: if the frequency is outside of the range [0, 7.5 GHz]
		"""
		
		if f_low < 0 or f_low > 7.5e9 or f_hi < 0 or f_hi > 7.5e9:
			raise ValueError("Frequencies must be between 0 Hz and 7.5 GHz")
			
		self.inst.write(":SENS:FREQ:STARt {}".format(f_low))
		self.inst.write(":SENS:FREQ:STOP {}".format(f_hi))
		
	
	def set_RBW(self, RBW):
		"""
		Set the resolution bandwidth.
		
		Args:
			RBW: The new resolution bandwidth, in the range 10 Hz to 1 MHz in 1-3-10 steps
		"""
		
		if RBW < 10 or RBW > 1e6:
			raise ValueError("RBW must be between 10 Hz and 1 MHz")
		# TODO: check if the RBW is a valid number (1-3-10 steps)
		
		self.inst.write(":SENS:BAND:RES {}".format(RBW))
		
	
	def enable_RF(self, state):
		"""
		Turn the RF preamp on or off.
		
		Args:
			state: True to enable the preamp
		"""
		
		if state:
			state_s = "1"
		else:
			state_s = "0"
			
		self.inst.write(":SENSE:POWER:RF:GAIN:STATE {}".format(state_s))
		
	def set_input_atten(self, atten):
		"""
		Set the value of the input attenuation, in dB.
		
		Args:
			atten (integer): The new attenuation, in the range [0, 30] dB.
		
		Raises:
			ValueError: if the attenuation level is not in the range [0, 30]
			TypeError: if the attenuation level is not an integer
		"""
		
		if atten < 0 or atten > 30:
			raise ValueError("Input attenuation must be between 0 and 30 dB")
		if not isinstance(atten, (int, long)):
			raise TypeError("Attenuation level must be an integer")
		
		self.inst.write(":SENSE:POWER:RF:ATT {}".format(atten))
	
	# Measurements
	def measure_trace(self):
		"""
		Measure a single trace from the spectrum analyzer.
		
		Returns:
			List of amplitudes in dBm at each frequency measured
		"""
		
		# Turn off continuous tracing
		self.inst.write(":INIT:CONT OFF")
		
		# Set up trace 1 to be read as ASCII
		self.inst.write(":TRACE1:MODE WRITE")
		self.inst.write(":FORM:TRAC:DATA ASCII")
		
		# Trigger once
		self.inst.write(":INIT")
		# Wait until done
		while (int(self.inst.query(":STATUS:OPERATION:CONDITION?")) & (1 << 3)):
			pass
		
		# Ask for data and process it
		dataString = self.inst.query(":TRACE:DATA? TRACE1")
		dataList = dataString.split(", ")
		dataList[0] = dataList[0].split()[1]
		amplitudes = [float(i) for i in dataList]
		
		# Also, find the frequencies
		#f_min = int(self.inst.query(":SENSE:FREQ:START?"))
		#f_max = int(self.inst.query(":SENSE:FREQ:STOP?"))
		#freq = numpy.linspace(f_min, f_max, len(amplitudes))

		return amplitudes


		
if __name__ == '__main__':
	# Connect to our spectrum analyzer
	print "Connecting..."
	test = DSA815()
	test.conn("USB0::0x1AB1::0x0960::DSA8A134700016::INSTR")
	
	print "Configuring..."
	test.TG_enable(False)
	test.enable_RF(True)
	test.set_input_atten(0)
	test.set_freq_limits(1e6, 601e6)
	test.set_RBW(10e3)
	
	print("Measuring...")
	
	amp = test.measure_trace()
	print amp
	