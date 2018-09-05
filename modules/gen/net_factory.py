from core.tipping_element import cusp
from core.coupling import linear_coupling
from core.tipping_network import tipping_network

from random import randint

import networkx as nx

"""net_factory module"""

class net_factory():
    """net_factory class that provides functions to generate user defined
    networks from parameters"""
    def __init__(self):
        pass
    def create_one_cusp(self,a,b,c,initial_state):
        tc0 = cusp(0,a,b,c)
        tc0.update_state(initial_state)
        net = tipping_network()
        net.add_node(0,data=tc0)
        return net

    def create_cusp_chain(
            self,number,a,b,c,initial_state,cpl_strength,opt='uniform'
            ):
        if opt == 'uniform':
            pass
        else:
            raise ValueError( 'Unrecognized option ' + opt )
        
        net = tipping_network()
        for id in range(0,number):
            tc = cusp(id,a,b,c)
            tc.update_state(initial_state)
            net.add_node(id,data=tc)

        for id in range(1,number):
            cpl = linear_coupling(net.nodes[id-1]['data']
                                 ,net.nodes[id]['data']
                                 ,cpl_strength)
            
            net.add_edge(id-1,id,weight=cpl_strength,data=cpl)
                        
        return net
    
    def create_two_cusps(self,a,b,c,initial_state,cpl_strength,negative_coupling=False):
        
        net = tipping_network()
        for id in range(0,2):
            tc = cusp(id,a,b,c)
            tc.update_state(initial_state)
            net.add_node(id,data=tc)

        if negative_coupling:
            m_cpl_strength = -cpl_strength
        else:
            m_cpl_strength = cpl_strength
        
        for id in range(1,2):
            cpl1 = linear_coupling(net.nodes[id-1]['data']
                                  ,net.nodes[id]['data']
                                  ,cpl_strength)
            cpl2 = linear_coupling(net.nodes[id]['data']
                                  ,net.nodes[id-1]['data']
                                  ,m_cpl_strength)
            
            net.add_edge(id-1,id,weight=cpl_strength,data=cpl1)
            net.add_edge(id,id-1,weight=m_cpl_strength,data=cpl2)
                        
        return net
    
    def create_butterfly(self,wing_number,wing_size,a,b,c,initial_state,cpl_strength):
        net = tipping_network()
        net_size = wing_number*(wing_size - 1) + 1
        for id in range(0,net_size):
            tc = cusp(id,a,b,c)
            tc.update_state(initial_state)
            net.add_node(id,data=tc)
        
        id = 1
        for no in range(0,wing_number):
            cpl = linear_coupling(net.nodes[0]['data']
                                       ,net.nodes[id]['data']
                                       ,cpl_strength)
            net.add_edge(0,id,weight=cpl_strength,data=cpl)
            for k in range(2,wing_size):
                cpl = linear_coupling(net.nodes[id]['data']
                                       ,net.nodes[id+1]['data']
                                       ,cpl_strength)
                net.add_edge(id,id+1,weight=cpl_strength,data=cpl)
                id+=1
            cpl = linear_coupling(net.nodes[id]['data']
                                       ,net.nodes[0]['data']
                                       ,cpl_strength)
            net.add_edge(id,0,weight=cpl_strength,data=cpl)
            id+=1
        
        return net
    
    def create_ring(self,number,a,b,c,initial_state,cpl_strength):
        net = tipping_network()
        for id in range(0,number):
            tc = cusp(id,a,b,c)
            tc.update_state(initial_state)
            net.add_node(id,data=tc)
        
        for id in range(1,number):
            cpl = linear_coupling(net.nodes[id-1]['data']
                                 ,net.nodes[id]['data']
                                 ,cpl_strength)
        
            net.add_edge(id-1,id,weight=cpl_strength,data=cpl)
            
        cpl = linear_coupling(net.nodes[number-1]['data']
                                 ,net.nodes[0]['data']
                                 ,cpl_strength)
        
        net.add_edge(number-1,0,weight=cpl_strength,data=cpl)
        
        return net
        
    def create_erdos_renyi(
            self,num,average_degree,a,b,c,initial_state,cpl_strength,
            negative_coupling=False,seed=None
            ):
        prob = average_degree/(num-1)
        net = nx.erdos_renyi_graph(num, prob,seed=seed,directed=True)
        net.__class__ = tipping_network
        tc = cusp
        for id in net.nodes():
            tc = cusp(id,a,b,c)
            tc.update_state(initial_state)
            net.node[id]['data'] = tc
            
        for id in net.edges():
            if negative_coupling:
                if randint(0,1):
                    net.edges[id]['weight'] = cpl_strength
                else:
                    net.edges[id]['weight'] = -cpl_strength
            else:
                net.edges[id]['weight'] = cpl_strength
            
        return net