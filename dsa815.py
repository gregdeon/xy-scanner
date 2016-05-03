'''
dsa815.py
Controls a DSA815 spectrum analyzer.
Adapted from Colin O'Flynn's DSA815 module (github.com/colinoflynn/dsa815)

Author: Greg d'Eon
Date: May 3
'''

import visa

class DSA815(object):
	def __init__(self):
		pass

	def conn(self, constr="USB0::0x1AB1::0x0960::DSA8Axxxxxxx::INSTR"):
		"""Attempt to connect to instrument"""
		rm = visa.ResourceManager()
		self.inst = rm.open_resource(constr)

	def identify(self):
		"""Return identify string which has serial number"""
		return self.inst.ask("*IDN?")

	def TG_enable(self, state):
		if state:
			tstate = "1"
		else:
			tstate = "0"

		self.inst.write(":OUTput:STATe %s\n"%tstate)

	def TG_amp(self, amp):
		"""Set the TG output amplitude power in dBm"""

		if amp > 0 or amp < -20:
			raise ValueError("Amplitude outside of allowed range -20dBm to 0dBm")
		
		self.inst.write(":SOUR:POW:LEV:IMM:AMPL %d\n"%amp)

	def set_span(self, span):
		self.inst.write(":SENS:FREQ:SPAN %d\n"%span)

	def set_centerfreq(self, freq):		
		self.inst.write(":SENS:FREQ:CENT %d\n"%int(freq))

	def dis(self):
		del self.inst

		
if __name__ == '__main__':
	# Connect to our spectrum analyzer
	test = DSA815()
	test.conn("USB0::0x1AB1::0x0960::DSA8A134700016::INSTR")
	
	print "Turning TG on, setting frequency"
	test.TG_enable(True)
	test.set_span(0)
	test.set_centerfreq(10E6)