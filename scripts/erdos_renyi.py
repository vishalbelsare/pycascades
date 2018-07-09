# Add modules directory to path
import sys
sys.path.append('../modules')

# global imports
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import time

# private imports
from gen.net_factory import net_factory
from core.evolve import net_evolve

net_factory = net_factory()
net = net_factory.create_erdos_renyi(100,1,-1,1,0,-1,0.2,67)

t0 = time.process_time()
pos=nx.random_layout(net)
nx.draw(net,pos,with_labels=True)
nx.draw_networkx_edge_labels(net,pos,edge_labels=nx.get_edge_attributes(net,'weight'))
plt.show()

t_graph_draw = time.process_time() - t0
print(t_graph_draw)

net_evolve = net_evolve(net)

# initialize time
t0 = time.process_time()
net_evolve.tip([0],0.005,0.01,100)
#net_evolve.integrate(0.1,100)
t_iteration = time.process_time() - t0
print(t_iteration)

plt.figure(1)
plt.subplot(211)
plt.plot(net_evolve.times,net_evolve.states)

plt.subplot(212)
plt.plot(net_evolve.times,np.array(net_evolve.pars)[:,0])
plt.show()