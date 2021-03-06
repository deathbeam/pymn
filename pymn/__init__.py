#!/usr/bin/env python
# coding: utf-8

from argparse import ArgumentParser
from functools import partial
from time import sleep

from mininet.clean import cleanup
from mininet.node import CPULimitedHost, RemoteController
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import switch
import topology

def runMininet(protocols, controller, topo, topo_arg, ovs_switch, pattern):
  # If no arguments passed, set the default values
  if protocols == None:  protocols = "OpenFlow13"
  if controller == None: controller = [ "127.0.0.1" ]
  if topo == None:       topo = "SwitchTopo"
  if topo_arg == None:   topo_arg = [ 1 ]
  if ovs_switch == None: ovs_switch = "OVSSwitch"
  if pattern == None:    pattern = "xscxx"

  # Create topology
  cur_topo = getattr(topology, topo)(*topo_arg)

  # Get switch type
  cur_switch = partial(getattr(switch, ovs_switch), protocols=protocols)

  # Prepare mininet
  net = None

  # Execute pattern
  delay = ""
  for c in pattern:
    if c == 's':
      # Create mininet object
      net = Mininet(switch=cur_switch, controller=None)
      net.buildFromTopo(cur_topo)

      # Create and add controllers
      for i, address in enumerate(controller):
        net.addController(RemoteController('c{0}'.format(i), address, 6653))

      # Start connections to controllers
      net.start()
    elif c == 'c':
      if net != None: CLI(net)
    elif c == 'x':
      if net != None:
        net.stop()
        net = None
      else:
        cleanup()
    elif c.isdigit():
      delay += c
    elif c == 'd':
      if delay == "": delay = "1"
      print("*** Waiting " + delay + " seconds")
      sleep(float(delay))
      delay = ""

def main(argv=None):
  setLogLevel('info')

  # Create argument parser
  parser = ArgumentParser()

  # Add parser arguments
  parser.add_argument('-c', '--controller',
      action='append', type=str)

  parser.add_argument('-a', '--topo-arg',
      action='append', type=int)

  parser.add_argument('-t', '--topo',
      nargs='?', const="SwitchTopo", type=str,
      help='LinearTopo, SwitchTopo, SingleSwitchTopo, SingleSwitchReversedTopo, TreeTopo (default: SwitchTopo)')

  parser.add_argument('-s', '--switch',
      nargs='?', const="OVSSwitch", type=str,
      help='OVSSwitch, UserSwitch, OVSLegacyKernelSwitch (default: OVSSwitch)')

  parser.add_argument('-p', '--protocols',
      nargs='?', const="OpenFlow13", type=str,
      help='OpenFlow10, OpenFlow13 (default: OpenFlow13)')


  parser.add_argument('-e', '--pattern',
      nargs='?', const='xscxx', type=str,
      help='s = start, c = console, {sec}d = delay, x = stop (default: xscxx)')

  # Parse arguments from command lin
  a = parser.parse_args(argv)

  runMininet(a.protocols, a.controller, a.topo, a.topo_arg, a.switch, a.pattern)
