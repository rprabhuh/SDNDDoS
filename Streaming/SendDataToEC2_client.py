#!/usr/bin/env python
import socket, sys

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *
from subprocess import call	


#CMD TO DUMP INCOMING/OUTGOING TCP DATA AT THE CONTROLLER - send to socket directly
proc = subprocess.Popen('sudo tshark -i wlan0 -T fields -e frame.number -e frame.interface_id -e frame.encap_type -e frame.offset_shift -e frame.time_epoch -e frame.time_delta -e frame.time_delta_displayed -e frame.time_relative -e frame.len -e frame.cap_len -e frame.marked -e frame.ignored -e frame.protocols -e ip.version -e ip.hdr_len -e ip.dsfield -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.len -e ip.id -e ip.flags -e ip.flags.rb -e ip.flags.df -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e ip.proto -e tcp.srcport -e tcp.dstport -e tcp.stream -e tcp.hdr_len -e tcp.flags -e tcp.flags.res -e tcp.flags.ns -e tcp.flags.cwr -e tcp.flags.ecn -e tcp.flags.urg -e tcp.flags.ack -e tcp.flags.push -e tcp.flags.reset -e tcp.flags.syn -e tcp.flags.fin -e tcp.window_size_value -e tcp.window_size -e tcp.window_size_scalefactor -e tcp.option_len -e tcp.options.timestamp.tsval -e tcp.options.timestamp.tsecr -e tcp.analysis.bytes_in_flight -e eth.lg -e eth.ig -e eth.type -e arp.hw.type -e arp.proto.type -e arp.hw.size -e arp.proto.size -e arp.opcode -E header=y -E separator=,',
			shell=True,
			stdin=subprocess.PIPE,
      stdout=subprocess.PIPE,		# Write to a buffer instead of a file/pipe
      stderr=subprocess.PIPE)


# Pre-process data
	''' by replacing NULLs with 0
	encoding categorical attributes'''


# Check/modify the following code to send the data from the pre-processed buffer to EC2

''' 
suppose array data[] contains the prepared data from the previous steps, 
now send each item in a for loop as a socket client.
actually the previous packet sampler is a socket server running in a 
while (True) loop to keep collecting data, and the Spark
part acts as a socket client.
'''

# hard-coded IP and port
# need to replace it with EC2 instance parameter
TCP_IP = '127.0.0.1'
TCP_PORT = 3000
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
for item in data
  s.send(item)
s.close()

