#!/usr/bin/env python
import socket
from scapy.all import *

# prepare the listening connection
TCP_IP = '127.0.0.1' 
#TCP_PORT = int(sys.argv[-1])
TCP_PORT = 3000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(20)

conn, addr = s.accept()
print 'Connection address:', addr

def pkt_callback(pkt):
  #pkt.show()
  if not IP in pkt:
    return "not IP"

  global conn

  # data fields: 
  # class label, length of ethernet frame, src IP, dst IP,
  # network layer protocol(UDP=1, else=0), src port, dst port,
  # monlist req(exist=1, otherwise=0)
  label = 1 if "\x17\x00\x03\x2a\x00\x00\x00\x00" in str(pkt[IP]) and len(pkt) <= 100 else 0
  output = [label, len(pkt), 
            1 if (UDP in pkt) else 0, pkt[IP].sport, pkt[IP].dport]
  if "\x17\x00\x03\x2a" in str(pkt[IP]):
    output.append(1)
  else:
    output.append(0)
  # do remember to append the newline char otherwise Spark will wait
  outputStr = ' '.join(map(str, output)) + '\n'
  conn.send(outputStr)
  print outputStr

sniff(iface="wlan0", prn=pkt_callback, filter="ip", store=0)

conn.close()
