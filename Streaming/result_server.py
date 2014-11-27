#!/usr/bin/env python
import socket
import simplejson

##### TODELETE: this is for debugging, should be remove when put together with other parts
import time

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 256

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
  # from Spark side
  # result = get_result()
  # result is a python map  
  result = {"pkt_id":22222, "allow": True}

  out = simplejson.dumps(result)
  conn.send(out)
  print out
  
  ##### TODELETE: this is for debugging, should be remove when put together with other parts
  time.sleep(1) # wait for 1 second

s.close()
