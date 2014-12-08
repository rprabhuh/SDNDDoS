#!/usr/bin/env python
import socket, sys
import subprocess, shlex
#from struct import unpack
#from encode_protocol import encode_protocol

TCP_IP = '127.0.0.1'
TCP_PORT = 3000
BUFFER_SIZE = 1024

#### function of parsing captured raw data
#### parsing one line of data from tshark
# 1) encode categorial data to numbers
# 2) encode hex data
#    the fields to encode: ip.dsfield.dscp, ip.dsfield.ecn, ip.id
# 3) encode NULL to 0
def parse_sample(line):
  if line is None or line == "":
    return ""

  NUM_FIELDS = 43
  SEPARATOR = ','
  fields = line[:-1].lower().split(SEPARATOR, NUM_FIELDS)

  # THE FIRST FIELD (frame.time_relative) CONTAINS THE UNIQUE
  # IDENTIFIER OF EACH PACKET AS IT WILL BE UNIQUE
  try:
    fields[0]
  except:
    return ""

  # 1) encode categorial data to numbers: fields[2] - ip.proto
  # fields[2] = str(encode_protocol(fields[2]))

  # Consider only TCP packets:
  # read the ip.proto to check for TCP (ip.proto = 6)
  # Send only TCP data to EC2
  if fields[2] != "6":
    return ""

  # 2) convert hex data to string:
  '''Hex fields present in the data: Entire feature set present at FeatureSet.txt
  fields[1]  - ip.id
  fields[14] - ip.dsfield.dscp
  fields[15] - ip.dsfield.ecn
  '''
  for i in [1,14,15]:
    fields[i] = '' + str(int(fields[i],16))
    #if len(fields[i]) >= 8:
    #  fields[i] = unpack('d', ''.join(fields[i]))

  # 3) encode NULL to 0;
  for i in range(len(fields)):
    if fields[i] == "":
      fields[i] = "0"

  # temporarily remove frame.encap_type field
  # for debugging
  if (len(fields) > 5):
    del fields[4]

  # return the parsed data
  out = ','.join(fields)
  if (len(out.split(',')) == 44):
    return out + '\n'
  else:
    return ""

########### Start of actual logic ###########

print "building capture command:"
CAPTURE_INTERFACE = 'wlan0'
cmd = 'sudo tshark -i ' + CAPTURE_INTERFACE + ' -T fields -e frame.time_relative -e ip.id -e ip.proto -e frame.interface_id -e frame.encap_type -e frame.offset_shift -e frame.time_epoch -e frame.time_delta -e frame.len -e frame.cap_len -e frame.marked -e frame.ignored -e ip.hdr_len -e ip.dsfield -e ip.dsfield.dscp -e ip.dsfield.ecn -e ip.len -e ip.flags.rb -e ip.flags.df -e ip.flags.mf -e ip.frag_offset -e ip.ttl -e tcp.stream -e tcp.hdr_len -e tcp.flags.res -e tcp.flags.ns -e tcp.flags.cwr -e tcp.flags.ecn -e tcp.flags.urg -e tcp.flags.ack -e tcp.flags.push -e tcp.flags.reset -e tcp.flags.syn -e tcp.flags.fin -e tcp.window_size_value -e tcp.window_size -e tcp.window_size_scalefactor -e tcp.option_len -e tcp.options.timestamp.tsval -e tcp.options.timestamp.tsecr -e tcp.analysis.bytes_in_flight -e eth.lg -e eth.ig -E separator=,'

print 'executing capture command'
proc = subprocess.Popen(shlex.split(cmd), shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# skip the first line, it is not data
proc.stdout.readline()

print 'Setting up connection to Spark:'
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# to handle Python [Errno 98] Address already in use
soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc.bind((TCP_IP, TCP_PORT))
soc.listen(5)

client_soc, addr = soc.accept()
print 'Connection address:', addr

while 1:
  sample = parse_sample(proc.stdout.readline())
  number_of_fields = len(sample.split(','))

  if number_of_fields > 1:
    print "sample=" + sample
  client_soc.send(sample)

client_soc.close()
soc.close()
net.stop()
