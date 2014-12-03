#!/usr/bin/env python
import socket, sys, simplejson
import subprocess, shlex

FLOW_BLOCKED = False

def find_host_from_pktid(pkt_id):
  return "10.0.0.1"

def block_host(host):
  global FLOW_BLOCKED
  if not FLOW_BLOCKED:
    print("=============== Flows before blocking: ===============")
    subprocess.call('ovs-ofctl dump-flows s1', shell=True)

    cmd = "ovs-ofctl add-flow s1 priority=11,dl_type=0x0800,nw_src=" + str(host) + ",action=drop"
    subprocess.call(cmd, shell=True)

    print("=============== Flows after blocking: ===============")
    subprocess.call('ovs-ofctl dump-flows s1', shell=True)

    print("=====================================================")
    FLOW_BLOCKED = True

def restore_host(host):
  global FLOW_BLOCKED
  if FLOW_BLOCKED:
    print("=============== Flows before restoring: ===============")
    subprocess.call('ovs-ofctl dump-flows s1', shell=True)

    cmd = 'ovs-ofctl --strict del-flows s1 priority=11,dl_type=0x0800,nw_src=' + str(host)
    subprocess.call(cmd, shell=True)

    print("=============== Flows after restoring: ===============")
    subprocess.call('ovs-ofctl dump-flows s1', shell=True)

# hard-coded IP and port for testing
TCP_IP = '127.0.0.1'
ANS_PORT = 3006
BUFFER_SIZE = 256

soc_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# to handle Python [Errno 98] Address already in use
soc_recv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
soc_recv.bind((TCP_IP, ANS_PORT))
soc_recv.listen(5)

conn, addr = soc_recv.accept()
print 'Connection address:', addr

while 1:
  data = conn.recv(BUFFER_SIZE)
  result = simplejson.loads(data)
  print result
  """ result looks something like this:
  {"pkt_id": "23.4567", "allow": True}
  """
  if not result["allow"]:
    host_to_block = find_host_from_pktid(result["pkt_id"])
    block_host(host_to_block)
  else:
    print "normal traffic"

soc_recv.close()
conn.close()
