import math
import random
import os
import matplotlib.pyplot as pyplot
import DirectedGraphWorld
from DirectedGraph import *
"""
In this file we will generate some figures to get some interesting results
with graphs.
"""

def etime():
    """gets the time at the moment it's called"""
    user, sys, chuser, chsys, real = os.times()
    return user+sys


def knotting_order_of_growth():
    mo = 10
    times = []
    vs = []
    trues = []
    swdg = SmallWorldDirectedGraph(mo)
    for i in range(2000):
        swdg.single_time_step()
        start = etime()
        flag = swdg.has_knot()
        end = etime()
        if flag:
            trues.append(1)
        else:
            trues.append(0)
        vs.append(mo+i)
        elapsed = end - start
        times.append(elapsed)
    pyplot.figure(1)
    pyplot.subplot(211)
    pyplot.plot(vs,times)
    pyplot.xlabel('# of vertices')
    pyplot.ylabel('knotting runtime')
    #~ pyplot.subplot(212)
    #~ pyplot.plot(vs,trues,'o')
    #~ pyplot.xlabel('# of vertices')
    #~ pyplot.ylabel('has a knot')
    pyplot.show()

def ErdosRenyiClustering():
    """
    Creates an Erdos-Renyi graph of 1000 vertices and iterates through
    p, checking the clustering coefficient each time. Uses pylot to
    graph all that stuff, to see if there's anything interesting
    """
    import matplotlib.pyplot as pyplot
    vs = [Vertex(str(v)) for v in range(100)]
    cs = []
    ps = []
    p = 0.01
    for i in range(100):
        drg = DirectedGraph(vs)
        drg.add_random_arcs(p)
        ps.append(p)
        cs.append(drg.clustering_coefficient())
        p += 0.01
    pyplot.plot(ps,cs)
    pyplot.xlabel('p')
    pyplot.ylabel('clustering coefficient')
    pyplot.show()

def WattsStrogatzClustering():
    """
    Creates an Erdos-Renyi graph of 1000 vertices and iterates through
    p, checking the clustering coefficient each time. Uses pylot to
    graph all that stuff, to see if there's anything interesting
    """
    import matplotlib.pyplot as pyplot
    import numpy
    vs = [Vertex(str(v)) for v in range(100)]
    cs = []
    ps = list(numpy.logspace(start=-5,stop=0,num=10))
    for p in ps:
        drg = WattsStrogatzSmallWorldDirectedGraph(1000,10,p)
        cs.append(drg.clustering_coefficient())
    c_zero = cs[0]
    cs = [item/c_zero for item in cs]
    pyplot.plot(ps,cs,'o')
    pyplot.xlabel('p')
    pyplot.xscale('log')
    pyplot.ylabel('clustering coefficient')
    pyplot.show()

def BarabasiAlbertClustering():
    """
    Creates an Erdos-Renyi graph of 1000 vertices and iterates through
    p, checking the clustering coefficient each time. Uses pylot to
    graph all that stuff, to see if there's anything interesting
    """
    import matplotlib.pyplot as pyplot
    import numpy
    cs = []
    ts = list(numpy.logspace(start=1,stop=3,num=10))
    for t in ts:
        swdg = SmallWorldDirectedGraph(1000)
        swdg.build_graph(int(t))
        print t
        cs.append(swdg.clustering_coefficient())
    #~ c_zero = cs[0]
    #~ cs = [item/c_zero for item in cs]
    pyplot.plot(ts,cs,'o')
    pyplot.xlabel('time steps')
    pyplot.xscale('log')
    pyplot.ylabel('clustering coefficient')
    pyplot.show()
    
def ErdosRenyiKnotting():
    """
    Finds the relationship between the probability in an Erdos Renyi graph (p)
    and the odds that this graph has a knot.
    """
    for num_vert in [5,15,30]:
        p = .01
        ps = []
        vs = [Vertex(str(v)) for v in range(num_vert)]
        ys = []
        for k in range(100):
            knot_count = 0
            for i in range(100):
                drg = DirectedGraph(vs)
                drg.add_random_arcs(p)
                #~ c = CircleLayout(drg)
                
                if drg.has_knot():
                    knot_count += 1
            knot_prob = knot_count/100.0
            ys.append(knot_prob)
            ps.append(p)
            p += .01
        pyplot.figure(1)
        pyplot.plot(ps,ys,'o')
        pyplot.xlabel('p')
        pyplot.ylabel('Odds of having a knot')
    pyplot.legend(('5 Vertices','15 Vertices','30 Vertices'))
    pyplot.show()
    
def WattsStrogatzKnotting():
    """
    Testing the probability of having a knot in a Watt-Strogatz
    Small World Graph. 
    Turns out WattsStrogatz Graphs always have knots. Interesting
    Result? I don't think so.
    """
    for i in range(50):
        dg = WattsStrogatzSmallWorldDirectedGraph(5,4,1)
        if not dg.has_knot():
            print 'woah'
    print 'nah'
    #~ DirectedGraphWorld.show_directed_graph(dg)

#~ def BarabasiAlbertClustering():
    

def BarabasiAlbertKnotting():
    for num_graphs in range(5):
        mo = 5
        t = 1
        num_graphs = 100
        ts = []
        knots = []
        for i in range(30):
            knot_count = 0
            for j in range(num_graphs):
                swdg = SmallWorldDirectedGraph(mo)
                swdg.build_graph(t)
                if swdg.has_knot():
                    knot_count += 1
                del swdg
            knots.append(knot_count/(float(num_graphs)))
            ts.append(t)
            print t
            t = int(t+3)
        pyplot.figure(1)
        pyplot.plot(ts,knots)
        pyplot.xlabel('Time Steps')
        pyplot.ylabel('Probability of having a knot')
        #~ mo += 1
    pyplot.show()


if __name__ == '__main__':
    #~ WattsStrogatzClustering()
    BarabasiAlbertClustering()
    

