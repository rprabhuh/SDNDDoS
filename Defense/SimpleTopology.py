#!/usr/bin/env python
from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from subprocess import call

net = Mininet()
#cli=CLI()
#Creating nodes in the network
c0=net.addController()
h0=net.addHost('h0')
s1=net.addSwitch('s1')
h1=net.addHost('h1')
h2=net.addHost('h2')
#Creating links between nodes in network (2-ways)
net.addLink(h0,s1)
net.addLink(h1,s1)
net.addLink(h2,s1)

net.start()
#Addition of the flow rule
print("Flow Rule Added")
call( 'ovs-ofctl add-flow s1 priority=10,action=normal', shell=True )
net.pingAll()

#To stop the flow from host 0  with ip 10.0.0.1
print("Stop the flow from host 0  with ip 10.0.0.1")
call( 'ovs-ofctl add-flow s1 priority=11,dl_type=0x0800,nw_src=10.0.0.1,action=drop', shell=True ) 
net.pingAll()

#To restore the flo back for host 0 after quarantine
print("Restore communication with the host 0")
call( 'ovs-ofctl --strict del-flows s1 priority=11,dl_type=0x0800,nw_src=10.0.0.1', shell=True )
net.pingAll()

CLI(net)
net.stop()
