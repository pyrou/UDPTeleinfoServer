# UDPTeleinfoServer

UDP server that is listening for raw "Teleinfo" (EDF) datagrams

## Usage

`UDPTeleinfoServer.py` can be used standalone to decode and print out received "Teleinfo" datagrams

```bash
Usage: python ./UDPTeleinfoServer.py [-p <port>] [-H <host>]

Options:
  -p, --port     Specify on which port the server is listening
  -H, --host     Specify on which host the server is listening
```

## Example

On the server, run foolowing command :

```bash
# python ./UDPTeleinfoServer.py -p 8000
```

Server is now listening incomming datagrams on port `8000`

To test the server, try this command on any machine on the same LAN

```bash
echo -en "MOTDETAT 000000 B\r\nADCO 200000294579 =\r\nOPTAR\
IF BASE 0\r\nISOUSC 30 9\r\nBASE 002565285 ,\r\nPTEC TH.. $\
\r\nIINST 002 Y\r\nIMAX 030 B\r\nPAPP 00420 '\r\n\x03" \
| socat - UDP-DATAGRAM:255.255.255.255:8000,broadcast
```

The expected output on the server is :
```python
{'IINST': '002', 'OPTARIF': 'BASE', 'ADCO': '200000294579',
'MOTDETAT': '000000', 'PAPP': '00420', 'BASE': '002565285',
'IMAX': '030', 'PTEC': 'TH..', 'ISOUSC': '30'}
```

Server still accept further datagrams
