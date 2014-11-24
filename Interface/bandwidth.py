#!/usr/bin/env python
import pico
import time

# Interface to monitor
IFACE = 'wlan0'
# Update rate (seconds)
RATE = 0.2

# read the local file system
def get_current(iface):
  # Parse out required interface
  f = open('/proc/net/dev', 'r')
  all = f.readlines();
  f.close()

  for dev in all:
    dev = dev.strip().replace(':',' ').split()
    if dev[0] == iface:
      # Return current throughput bytes for rx/tx
      return (int(dev[1]), int(dev[9]))

  return None

# this is the function called by pico
def rx():
  (rx1, tx1) = get_current(IFACE)
  time.sleep(RATE)
  (rx2, tx2) = get_current(IFACE)
  if rx1 and rx2:
    return (rx2 - rx1) * 8 * 1.0e-3 / RATE
  else:
    return 0

# the following functions are for testing
def measure(iface, rate):
  (rxlast, txlast) = (None, None)
  while 1:
    (rx, tx) = get_current(iface)
    if rxlast and txlast:
      # Calculate bandwidth and push to database
      bwrx = (rx - rxlast) * 8 * 1.0e-3 / rate
      bwtx = (tx - txlast) * 8 * 1.0e-3 / rate
      print "rx: " + str(bwrx) + "kb/s, tx = " + str(bwtx) + "kb/s"      
    (rxlast, txlast) = (rx, tx)
    time.sleep(rate)

if __name__ == "__main__":
  measure(IFACE, RATE)
