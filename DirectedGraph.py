from Graph import Graph, Vertex, Edge

class DirectedVertex(Vertex):
    pass

class DirectedEdge(Edge):
    def __repr__(self):
        """Return a string representation of the edge thisedge that can be
        evaluated as a Python expression."""
        return 'Edge(%s to %s)' %(repr(self[0]), repr(self[1]))

class DirectedGraph(Graph):

    def __init__(self,vs=[],es=[]):
        """Creates a new directed graph."""
        self.inverse_graph = {} #maps in_edges. (key=vertex, val=dictionary of incoming vertices
        for v in vs:
            self.add_vertex(v)
        for e in es:
            self.add_edge(e)
 
    def add_vertex(self, v):
        self[v] = {}
        self.inverse_graph[v] = {}
    
    def add_edge(self, e):
        """
        Creates an edge FROM V TO W (in V's first dictionary).
        Adds same edge TO W FROM V (in W's second dicionary).
        """
        v, w = e
        self[v][w] = e
        self.inverse_graph[w][v] = e
        
    def get_out_edge(self, v, w):
        """
        Tries to return the directed edge FROM V TO W. If no edge exists,
        returns None.
        """
        try:
            return self[v][w]
        except KeyError:
            return None

    has_out_edge = get_out_edge
    
    def get_in_edge(self, v, w):
        """
        Tries to return the directed edge TO V FROM W. Returns None if no such
        edge exists.
        """
        try:
            return self.inverse_graph[v][w]
        except KeyError:
            return None
    
    has_in_edge = get_out_edge

    def remove_edge(self, v, w):
        """Deletes the directed edge FROM V TO W."""
        del self[v][w]
        del self.inverse_graph[w][v]

    def edges(self):
        s = set()
        for d in self.itervalues():
            s.update(d.itervalues())
        return s
    
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
            return len(self.inverse_graph[v])
        except KeyError:
            return None
