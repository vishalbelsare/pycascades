# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
import matplotlib.pyplot as plt
import networkx as nx

# private imports
from gen.net_factory import net_factory
from core.integrate import solver

net_factory = net_factory()
net = net_factory.create_oscillator(-1,1,0,-1,0.5)
pos=nx.spring_layout(net)
nx.draw_networkx(net,pos)
nx.draw_networkx_edge_labels(net,pos,edge_labels=nx.get_edge_attributes(net,'weight'))
plt.show()

solver = solver(net)

# initialize time
solver.iterate(net.nodes[0]['data'],100,0.01,0.001)

plt.figure(1)
plt.subplot(211)
plt.plot(solver.times,solver.states)

plt.subplot(212)
plt.plot(solver.pars,solver.states)
plt.show()

