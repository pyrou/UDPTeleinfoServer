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
{"IINST": "002", "OPTARIF": "BASE", "ADCO": "200000294579", "MOTDETAT": "000000",
 "PAPP": "00420", "BASE": "002565285", "IMAX": "030", "timestamp": 1421919714,
"PTEC": "TH..", "ISOUSC": "30"}
"""
from __future__ import print_function

import socket, getopt, sys, json, time
import TeleinfoParser

def main(argv):
	("Usage: python ./UDPTeleinfoServer.py [-p <port>] [-H <host>] [-w <wait_delay>]\n\n"
	 "Options:\n"
	 "  -p, --port     Specify on which port the server is listening\n"
	 "  -H, --host     Specify on which host the server is listening\n"
	 "  -w, --wait     Time in seconds to wait between reading two datagrams. During\n"
 	 "                 the wait time, datagrams received are dropped. The default\n"
	 "                 value is 0")
	port = 10000
	host = "0.0.0.0"
	wait = 0

	try:
		opts, args = getopt.getopt(argv,"hp:H:w:",["help","port=","host=","wait="])
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				print(main.__doc__)
				sys.exit()
			elif opt in ("-p", "--port"):
				port = int(arg)
			elif opt in ("-w", "--wait"):
				wait = int(arg)
			elif opt in ("-H", "--host"):
				host = arg

	except (getopt.GetoptError, ValueError):
		print(main.__doc__, file=sys.stderr)
		sys.exit(2)

	print('Server listing on ' + host + ':' + str(port) + ' (Ctrl+C to stop)', file=sys.stderr)
	server = UDPTeleinfoServer(port=port, host=host, wait_delay=wait);
	try:
		while True:
			print(json.dumps(server.read()))
	except KeyboardInterrupt:
		server.close();
		pass

class UDPTeleinfoServer:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	parser = TeleinfoParser.TeleinfoParser()

	def __init__ (self, port=10000, host='', wait_delay=0):
		self.sock.bind((host, port))
		self.last = 0
		self.wait_delay = wait_delay

	def close (self):
		"""Close the socket"""
		self.sock.close();

	def read (self):
		"""Read and verify Teleinfo datagram and return it as a dict"""
		message, address = self.sock.recvfrom(1024)
		if self.wait_delay > 0 and int(time.time()) - self.last < self.wait_delay:
			return self.read()

		data = self.parser.parse(message)
		data['timestamp'] = self.last = int(time.time())
		return data

if __name__ == '__main__':
	main(sys.argv[1:])
