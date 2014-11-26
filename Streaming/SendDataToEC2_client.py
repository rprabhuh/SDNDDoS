#!/usr/bin/env python
import socket, sys
import subprocess, shlex

# TODO: parsing one line of data from tshark
# need to:
# 1) encode hex data using unpack:
# http://stackoverflow.com/questions/3531723/unpack-from-hex-to-double-in-python
# 2) encode NULL to 0;
# 3) encode categorial data to numbers
def parseSample(line):
  return line

# connect as a TCP *client*
# should ideally be a server, because Spark should be the client
# but making this part a client is easier than letting EC2 connect
# to a machine inside university network
  
# hard-coded IP and port
# need to replace it with EC2 instance parameter
TCP_IP = '127.0.0.1'
TCP_PORT = 3000
BUFFER_SIZE = 1024
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((TCP_IP, TCP_PORT))

cmd = shlex.split('sudo tshark -i wlan0 -T fields -e frame.number -e frame.interface_id -e frame.encap_type -e frame.offset_shift -e frame.time_epoch -e frame.time_delta -e frame.time_delta_displayed -e frame.time_relative -e frame.len -e frame.cap_len -e frame.marked -e frame.ignored -e frame.protocols -e ip.version -e ip.hdr_len -e ip.dsfield -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.len -e ip.id -e ip.flags -e ip.flags.rb -e ip.flags.df -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e ip.proto -e tcp.srcport -e tcp.dstport -e tcp.stream -e tcp.hdr_len -e tcp.flags -e tcp.flags.res -e tcp.flags.ns -e tcp.flags.cwr -e tcp.flags.ecn -e tcp.flags.urg -e tcp.flags.ack -e tcp.flags.push -e tcp.flags.reset -e tcp.flags.syn -e tcp.flags.fin -e tcp.window_size_value -e tcp.window_size -e tcp.window_size_scalefactor -e tcp.option_len -e tcp.options.timestamp.tsval -e tcp.options.timestamp.tsecr -e tcp.analysis.bytes_in_flight -e eth.lg -e eth.ig -e eth.type -e arp.hw.type -e arp.proto.type -e arp.hw.size -e arp.proto.size -e arp.opcode -E header=y -E separator=,')

proc = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# proc = subprocess.Popen(['ping', 'google.com'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# skip the first line, it is not data
proc.stdout.readline()

# keep reading and sending
while 1:
  item = parseSample(proc.stdout.readline())
  soc.send(item)

soc.close()

