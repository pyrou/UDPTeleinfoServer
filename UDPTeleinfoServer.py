#!/usr/bin/env python

"""
UDPTeleinfoServer

UDP Server that is listening for Teleinfo (EDF) datagrams

Can be tested with socat :
echo -en "MOTDETAT 000000 B\r\nADCO 200000294579 =\r\nOPTAR\
IF BASE 0\r\nISOUSC 30 9\r\nBASE 002565285 ,\r\nPTEC TH.. $\
\r\nIINST 002 Y\r\nIMAX 030 B\r\nPAPP 00420 '\r\n\x03" \
| socat - UDP-DATAGRAM:255.255.255.255:10000,broadcast

Expected output :
{'IINST': '002', 'OPTARIF': 'BASE', 'ADCO': '200000294579',
'MOTDETAT': '000000', 'PAPP': '00420', 'BASE': '002565285',
'IMAX': '030', 'PTEC': 'TH..', 'ISOUSC': '30'}
"""
from __future__ import print_function

import socket, getopt, sys

def main(argv):
	("Usage: python ./UDPTeleinfoServer.py [-p <port>] [-H <host>]\n\n"
	 "Options:\n"
	 "  -p, --port     Specify on which port the server is listening\n"
	 "  -H, --host     Specify on which host the server is listening")
	try:
		opts, args = getopt.getopt(argv,"hp:H:",["help","port=","host="])
		port = 10000
		host = "0.0.0.0"
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				print(main.__doc__)
				sys.exit()
			elif opt in ("-p", "--port"):
				port = int(arg)
			elif opt in ("-H", "--host"):
				host = arg
	except (getopt.GetoptError, ValueError):
		print(main.__doc__, file=sys.stderr)
		sys.exit(2)

	print('Server listing on ' + host + ':' + str(port) + ' (Ctrl+C to stop)', file=sys.stderr)
	server = UDPTeleinfoServer(port=port, host=host);
	try:
		while True: print(server.read())
	except KeyboardInterrupt:
		pass

class UDPTeleinfoServer:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def __init__ (self, port=10000, host=''):
		self.sock.bind((host, port))

	def checksum (self, label, value):
		"""Return the checksum of a value and label"""
		sum = 32
		for c in label + value: sum += ord(c)
		return chr((sum & 63) + 32)

	def close (self):
		"""Close the socket"""
		self.sock.close();

	def read (self):
		"""Read and verify Teleinfo datagram and return it as a dict"""
		message, address = self.sock.recvfrom(1024)
		trames = [trame.split(" ") for trame in message.strip("\r\n\x03\x02").split("\r\n")]
		return dict([
			[trame[0],trame[1]] for trame in trames
			if (len(trame) == 3) and (self.checksum(trame[0],trame[1]) == trame[2])
			])

if __name__ == '__main__':
	main(sys.argv[1:])
