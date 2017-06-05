from mininet.topo import Topo
from mininet.util import irange

class SwitchTopo(Topo):
    def build(self, k=2, **opts):
        self.k = k
        lastSwitch = None

        for i in irange(1, k):
            switch = self.addSwitch('s{0}'.format(i), dpid='{0:x}'.format(i))
            if lastSwitch != None: self.addLink(lastSwitch, switch)
            lastSwitch = switch
