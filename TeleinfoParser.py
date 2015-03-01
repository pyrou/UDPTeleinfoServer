#!/usr/bin/env python

class TeleinfoParser:

	integerKeys = [
		'ISOUSC', 'BASE', 'HCHC', 'HCHP', 'EJPHN', 'EJPHPM',
		'BBRHCJB', 'BBRHPJB', 'BBRHCJW', 'BBRHPJW', 'BBRHCJR', 'BBRHPJR',
		'PEJP', 'IINST', 'IINST1', 'IINST2', 'IINST3', 'ADPS', 'IMAX',
		'IMAX1', 'IMAX2', 'IMAX3', 'PAPP', 'ADIR1', 'ADIR2', 'ADIR3' ]

	def checksum (self, label, value):
		"""Return the checksum of a value and label"""
		sum = 32
		for c in label + value: sum += ord(c)
		return chr((sum & 63) + 32)

	def parse (self, message):
		"""Read and verify Teleinfo datagram and return it as a dict"""
		trames = [trame.split(" ", 2) for trame in message.strip("\r\n\x03\x02").split("\r\n")]
		return dict([
			[trame[0], int(trame[1]) if trame[0] in self.integerKeys else trame[1]] for trame in trames
			if (len(trame) == 3) and (self.checksum(trame[0],trame[1]) == trame[2])
			])
