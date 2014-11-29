#!/usr/bin/env python

import socket
from time import sleep
from random import randint

text_file = open("Streaming_Classification_small.txt", "r")
lines = text_file.readlines()
filelen = len(lines)

TCP_IP = '127.0.0.1'
TCP_PORT = 3000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(20)

conn, addr = s.accept()
print 'Connection address:', addr

while 1:
  line = lines[randint(0, filelen-1)]
  print line
  conn.send(line)
  sleep(1)
conn.close()
