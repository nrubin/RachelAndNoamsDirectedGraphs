from DirectedGraph import DirectedGraph,DirectedEdge,DirectedVertex,DirectedRandomGraph
from DirectedGraphWorld import DirectedGraphWorld, CircleLayout




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
    KnottingRandomness()
