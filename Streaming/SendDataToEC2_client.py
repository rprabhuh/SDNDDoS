#!/usr/bin/env python
import socket, sys
import subprocess, shlex
from struct import unpack
from encode_protocol import encode_protocol

NUM_FIELDS = 43
SEPARATOR = ','

# parsing one line of data from tshark
# 1) encode categorial data to numbers
# 2) encode hex data 
#    the fields to encode: ip.dsfield.dscp, ip.dsfield.ecn, ip.id
# 3) encode NULL to 0

def parse_sample(line):
  fields = line.lower().split(SEPARATOR, NUM_FIELDS)
  
  # THE FIRST FIELD (frame.time_relative) CONTAINS THE UNIQUE IDENTIFIER OF EACH PACKET AS IT WILL BE UNIQUE


  '''Hex fields present in the data: Entire feature set present at FeatureSet.txt
  fields[1] - ip.id
  fields[14] - ip.dsfield.dscp
  fields[15] - ip.dsfield.ecn
  '''

  # Consider only TCP packets: read the ip.proto to check for TCP (ip.proto = 6)
  # Send only TCP data to EC2
  try:
	fields[0]
  except:
	return ""

  if fields[2] != "6":
	return ""

  # 1) encode categorial data to numbers: fields[2] - ip.proto
  fields[2] = str(encode_protocol(fields[2]))
  
  # 2) convert hex data to string:
  for i in [1,14,15]:
    fields[i] = '' + str(int(fields[i],16))
    #if len(fields[i]) >= 8:
    #  fields[i] = unpack('d', ''.join(fields[i])) 
  
  # 3) encode NULL to 0;
  for i in range(len(fields)):
    if fields[i] == "":
      fields[i] = "0"
  
  # return the parsed data
  return ','.join(fields)

"""
connect as a TCP *client*
should ideally be a server, because Spark should be the client
but making this part a client is easier than letting EC2 connect
to a machine inside university network
"""
# hard-coded IP and port for testing
#TCP_IP = '127.0.0.1'
#TCP_PORT = 3000

# EC2 instance socket address taken as cmd line arguments
TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])


BUFFER_SIZE = 1024
#soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#soc.connect((TCP_IP, TCP_PORT))

# RUN tshark COMMAND
cmd = shlex.split('sudo tshark -i vboxnet0 -T fields -e frame.time_relative -e ip.id -e ip.proto -e frame.interface_id -e frame.encap_type -e frame.offset_shift -e frame.time_epoch -e frame.time_delta -e frame.len -e frame.cap_len -e frame.marked -e frame.ignored -e ip.hdr_len -e ip.dsfield -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.len -e ip.flags.rb -e ip.flags.df -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e tcp.stream -e tcp.hdr_len -e tcp.flags.res -e tcp.flags.ns -e tcp.flags.cwr -e tcp.flags.ecn -e tcp.flags.urg -e tcp.flags.ack -e tcp.flags.push -e tcp.flags.reset -e tcp.flags.syn -e tcp.flags.fin -e tcp.window_size_value -e tcp.window_size -e tcp.window_size_scalefactor -e tcp.option_len -e tcp.options.timestamp.tsval -e tcp.options.timestamp.tsecr -e tcp.analysis.bytes_in_flight -e eth.lg -e eth.ig -E separator=,')

proc = subprocess.Popen(cmd, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# proc = subprocess.Popen(['ping', 'google.com'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# skip the first line, it is not data
#proc.stdout.readline()

# keep reading and sending
f = open("test.txt", "w")
while 1:
  item = parse_sample(proc.stdout.readline())
  if item == "":
	continue
 
  f.write(item)
  
  # item CONTAINS THE PACKET INFO TO BE SENT TO EC2 WHEREIN THE 1ST FIELD CONTAINS THE ip.id FIELD THAT UNIQUELY IDENTIFIES THIS PACKET
  #soc.send(item)

soc.close()

