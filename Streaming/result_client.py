#!/usr/bin/env python
import socket
import simplejson

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while 1:
  data = s.recv(BUFFER_SIZE)
  result = simplejson.loads(data)
  print result

s.close()
