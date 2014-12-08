#!/usr/bin/env python
import socket, fcntl, struct
import time
import subprocess, shlex

def get_ip_address(ifname):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  return socket.inet_ntoa(fcntl.ioctl(
                          s.fileno(),
                          0x8915,  # SIOCGIFADDR
                          struct.pack('256s', ifname[:15])
                          )[20:24])

ipaddr = get_ip_address('wlan0')

cmd = shlex.split('hping3 --rand-source ' + str(ipaddr) + 
                  ' -c 50 -i u10000 -S -L 0 -p 80')

while 1:
  proc = subprocess.call(cmd, shell=False)
  time.sleep(15)

