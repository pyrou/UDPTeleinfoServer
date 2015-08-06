# UDPTeleinfoServer

[![Code Climate](https://codeclimate.com/github/pyrou/UDPTeleinfoServer/badges/gpa.svg)](https://codeclimate.com/github/pyrou/UDPTeleinfoServer)

UDP server that is listening for raw "Teleinfo" (EDF) datagrams

## Usage

`UDPTeleinfoServer.py` can be used standalone to decode and print out received "Teleinfo" datagrams

```text
Usage: python ./UDPTeleinfoServer.py [-p <port>] [-H <host>]

Options:
  -p, --port     Specify on which port the server is listening
  -H, --host     Specify on which host the server is listening
  -w, --wait     Time in seconds to wait between reading two datagrams. During
                 the wait time, datagrams received are dropped. The default
                 value is 0
```

## Example

On the server, run following command :

```bash
# python ./UDPTeleinfoServer.py -p 8000 -w 5
```

Server is now listening incomming datagrams on port `8000`. 
However, it will only handle one request per 5 seconds.

To test the server, try this command on any machine on the same LAN

```bash
echo -en "MOTDETAT 000000 B\r\nADCO 200000294579 =\r\nOPTAR\
IF BASE 0\r\nISOUSC 30 9\r\nBASE 002565285 ,\r\nPTEC TH.. $\
\r\nIINST 002 Y\r\nIMAX 030 B\r\nPAPP 00420 '\r\n\x03" \
| socat - UDP-DATAGRAM:255.255.255.255:8000,broadcast
```

The expected output on the server is :
```json
{"IINST": 2, "OPTARIF": "BASE", "ADCO": "200000294579", "MOTDETAT": "000000",
 "PAPP": 420, "BASE": 2565285, "IMAX": 30, "timestamp": 1421919714,
"PTEC": "TH..", "ISOUSC": 30}
```

Server still accept further datagrams.
