from Graph import Graph, Vertex, Edge
import random
from GraphWorld import GraphWorld,GraphCanvas,Layout,CircleLayout,RandomLayout
#~ from DirectedGraphWorld import DirectedGraphWorld

class DirectedVertex(Vertex):
    """
    Represents a Directed Vertex in a graph.
    Is identical to a regular vertex.
    """
    pass

class DirectedEdge(Edge):
    """
    Represents a Directed Edge FROM Directed Vertex v TO Directed Vertex w.
    """
    def __repr__(self):
        """Return a string representation of the edge this directed
        edge that can be evaluated as a Python expression."""
        return 'Edge(%s to %s)' %(repr(self[0]), repr(self[1]))

class DirectedGraph(Graph):

    def __init__(self,vs=[],es=[]):
        """
        Creates a new directed graph. 
        @Args:
            vs, a list of DirectedVertices 
            es, a list of DirectedEdges
        @Returns:
            None
        """
        self.reverse_graph = {} #keeps a map of in-vertices
        for v in vs:
            self.add_vertex(v)
        for e in es:
            self.add_edge(e)
 
    def add_vertex(self, v):
        """
        Adds a vertex to both the DirectedGraph and its internal complement
        dictionary, and initiates its value as an empty dictionary.
        @Args:
            A DirectedVertex v
        @Returns:
            None
        """
        self[v] = {}
        self.reverse_graph[v] = {}
    
    def add_edge(self, e):
        """
        Creates an edge FROM v TO w (As a value of v in the internal dictionary).
        Adds same edge TO w FROM v (As a value of w in the reverse dictionary).
        @Args:
            A DirectedEdge e
        @Returns: 
            None
        """
        v, w = e
        if v == w:
            raise LoopError('An Edge cannot exist from a vertex to itself.')
        self[v][w] = e
        self.reverse_graph[w][v] = e
        
    def get_out_edge(self, v, w):
        """
        Tries to return the directed edge FROM v TO w. If no edge exists,
        returns None.
        """
        try:
            return self[v][w]
        except KeyError:
            return None

    has_out_edge = get_out_edge
    
    def get_in_edge(self, v, w):
        """
        Tries to return the directed edge TO w FROM w. Returns None if no such
        edge exists.
        """
        try:
            return self.reverse_graph[v][w]
        except KeyError:
            return None
    
    has_in_edge = get_out_edge

    def remove_edge(self, v, w):
        """Deletes the directed edge FROM v TO w."""
        del self[v][w]
        del self.reverse_graph[w][v]

    def edges(self):
        """returns a set of all out-edges of the graph"""
        s = set()
        for d in self.itervalues():
            s.update(d.itervalues())
        return s
    
    def in_edges(self, v):
        """returns a set of all in-edges of the graph"""
        s = set()
        for w in self.reverse_graph[v]:
            s.update(self.reverse_graph[v][w])
        return s

    def out_edges(self, v):
        """
        returns the edges leaving v
        """
        return self[v].values()

    def out_degree(self,v):
        """takes a vertex and returns the number of 
        edges leaving it (the out-degree)"""
        try:
            return len(self[v])
        except KeyError:
            return None
    
    def in_degree(self,v):
        """takes a vertex and returns the number
        of edges going into it (the in-degree)"""
        try:
            return len(self.reverse_graph[v])
        except KeyError:
            return None



    def is_strongly_connected(self):
        """iterates through every vertex in the graph, checking
        connectedness. If the graph is connected through every vertex,
        the the  directed graph is strongly connected."""
        def visit(v):
            self.visited_count += 1

        for v in self.vertices():
            v.visited = False
            
        for v in self.vertices():
            self.visited_count = 0
            for x in self.vertices():
                x.visited = False
            s = v

            self.bfs(s, visit = visit)

            if self.visited_count != len(self.vertices()):
                self.visited_count = None
                return False
        self.visited_count = None
        return True
    
    def complete(self):
        """completes the graph by adding an edge from every vertex
        to every vertex"""
        for v in self.vertices():
            current_vertex = v
            for w in self.vertices():
                if current_vertex == w:
                    continue
                e = DirectedEdge(current_vertex,w)
                self.add_edge(e)
                
    def is_complete(self):
        """checks if a graph is complete by ensuring that
        every vertex is adjacent to every other vertex in
        the graph"""
        for v in self.vertices():
            out_vertices = self.out_vertices(v)
            if len(out_vertices) != len(self.vertices())-1:
                return False
        return True
        
    def cluster(self, v):
        """
        Helper function for self.clustering_coefficient.
        Calculates the clustering coefficient around a vertex v,
        and returns it.
        """
        es = 0.0
        neighbors = self[v].keys()
        neighbors.extend(self.reverse_graph[v].keys())

        for w in neighbors:
            for u in neighbors:
                try:
                    self[w][u]
                    es += 1.0
                except KeyError:
                    pass

        k = len(self[v]) + len(self.reverse_graph[v])
        try: 
            c = es / (k * (k-1))
        except ZeroDivisionError:
            try:
                c = es / (k * 1)
            except ZeroDivisionError:
                c = 0
        return c

    def clustering_coefficient(self):
        """Calculates the clustering coefficient for a graph,
        and returns it."""
        local_cs = [self.cluster(v) for v in self.keys()]
        c = sum(local_cs) / len(local_cs)

        return c
        
    def _bfsknots(self, s):
        """
        Modified breadth-first search. Used to find knots.Returns the 
        set of vertices that are accessible by some path from s.

        s: start vertex
        """

        # initialize the queue with the start vertex
        queue = [s]
        visited = set()
        while queue:

            # get the next vertex
            v = queue.pop(0)

            # skip it if it's already marked
            if v in visited: continue

            # mark it visited, then invoke visit
            if v != s: visited.add(v)

            
            for x in self.out_vertices(v):
                
                #if its out vertices have been cached, update visited
                if x in self._knot_cache.keys():
                    visited.update(self._knot_cache[x])
                    visited.add(x)
                    
                #otherwise add its out vertices to the queue
                elif x not in self._knot_cache.keys():
                    queue.append(x)
                    
        self._knot_cache[s] = visited
        
        #ensures that s was not added to visited b/c of being in a cache
        if s in visited: self._knot_cache[s].remove(s)
        return visited

    def _knot_at_v(self, v):
        """
        Given a vertex v, finds whether each of its out vertices
        are all accessible from each other, and not accessible from
        any other vertex.
        
        Returns True if this is case; indicates v is entrance to knot.
        """
        t = self._knot_cache.get(v, None)

        if len(t) == 0:
            return False
            
        for w in self._knot_cache[v]:
                s = self._knot_cache.get(w, None)
                if len(s) == 0:
                    return False
                x = s.symmetric_difference(t)
                if x != set([v, w]):
                    return False

        return True

    def has_knot(self):
        """
        Returns true if directed graph has a knot.
        """
        self._knot_cache = {}
        #build the cache of which vertices are accessible from which
        for v in self:
            self._knot_cache[v] = self._bfsknots(v)

        #searches for knot
        for v in self:
            if self._knot_at_v(v):
                return True
        return False

    def add_regular_edges(self, k=2):
        """Make a regular directed graph with degree k if possible;
        otherwise raises an exception."""
        vs = self.vertices()
        if k >= len(vs):
            raise ValueError, ("cannot build a regular directed graph with " +
                               "degree >= number of vertices.")

        if (k%  2 == 1):
            raise ValueError, ("cannot build a regular directed graph with " +
                               "an odd degree")
        else:
            self.add_regular_edges_even(k)

    def add_regular_edges_even(self, k=2):
        """Make a regular directed graph with degree k.  k must be even"""
        vs = self.vertices()
        double = vs * 2
        
        for i, v in enumerate(vs):
            for j in range(1,k/2+1):
                w = double[i+j]
                self.add_edge(DirectedEdge(v, w))
                
    def rewire(self, p=0.01):
        """Rewires edges according to the algorithm in Watts and Strogatz.
        (p) is the probability that each edge is rewired.
        """
        # consider the edges in random order (this is slightly different
        # from Watts and Strogatz
        es = list(self.edges())
        random.shuffle(es)
        vs = self.vertices()
        
        for e in es:
            # if this edge is chosen, remove it...
            if random.random() > p: continue
            v, w = e
            self.remove_edge(v,w)

            # then generate a new edge that connects v to another vertex
            while True:
                w = random.choice(vs)
                if v is not w and not self.has_edge(v, w): break

            self.add_edge(DirectedEdge(v, w))
    
class DirectedRandomGraph(DirectedGraph):
    def add_random_edges(self, p=0.05):
        """Starting with an edgeless graph, add edges to
        form a random graph where (p) is the probability 
        that there is an edge between any pair of vertices.
        """
        vs = self.vertices()
        for i, v in enumerate(vs):
            for j, w in enumerate(vs):
                if v == w: continue
                if random.random() > p: continue
                self.add_edge(Edge(v, w))
        
class LoopError(Exception):
    """
    Vertices cannot have DirectedEdges leading to themselves. So we throw an error.
    """
    
    def __init__(self, value):
        self.parameter = value
        
    def __str__(self):
        return repr(self.parameter)
 
        
def show_graph(g):
    """
    Uses DirectedGraphWorld to show a DirectedGraph using Allen Downey's
    GraphWorld.
    """
    for v in g.vertices():
        """if v.visited: 
            v.color = 'white'
        else:
            v.color = 'red'"""
        v.color='red'

    layout = CircleLayout(g)
    gw = DirectedGraphWorld()
    gw.show_graph(g, layout)
    gw.mainloop()

    
    
        
    
        
if __name__ == '__main__':
    pass
    
    
    
    
