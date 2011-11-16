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

def small_world_knotting():
    mo = 5
    t = 5
    num_graphs = 100
    ts = []
    knots = []
    for i in range(1000):
        knot_count = 0
        for i in range(num_graphs):
            swdg = SmallWorldDirectedGraph(mo)
            swdg.build_graph(t)
            if swdg.has_knot():
                knot_count += 1
        knots.append(knot_count/(float(num_graphs)))
        ts.append(t)
        t += 1
    pyplot.figure(1)
    pyplot.plot(ts,knots,'o')
    pyplot.xlabel('Time Steps')
    pyplot.ylabel('Probability of having a knot')
    pyplot.show()

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

def SmallWorldTest():
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
        print p
        drg = DirectedRandomGraph(vs)
        drg.add_random_edges(p)
        ps.append(p)
        cs.append(drg.clustering_coefficient())
        p += 0.01
    pyplot.plot(ps,cs)
    pyplot.xlabel('p')
    pyplot.ylabel('clustering coefficient')
    pyplot.show()
    
def KnottingRandomness():
    """
    Takes the number of vertices each graph should have
    Finds the relationship between the probability in an Erdos Renyi graph (p)
    and the odds that this graph has a knot.
    """
    p = .01
    ps = []
    vs = [DirectedVertex(str(v)) for v in range(15)]
    ys = []
    for k in range(100):
        knot_count = 0
        for i in range(100):
            drg = DirectedRandomGraph(vs)
            drg.add_random_edges(p)
            #~ c = CircleLayout(drg)
            
            if drg.has_knot():
                knot_count += 1
        ys.append(knot_count/100.0)
        ps.append(p)
        p += .01
    import matplotlib.pyplot as pyplot
    pyplot.plot(ps,ys,'o')
    pyplot.xlabel('p')
    pyplot.ylabel('Odds of having a knot')
    pyplot.show()
    
    
    
    

if __name__ == '__main__':
    knotting_order_of_growth()

