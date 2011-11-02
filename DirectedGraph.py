from Graph import Graph, Vertex, Edge
#import GraphWorld

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
        if v == w:
			raise LoopError('An Edge cannot exist from a vertex to itself.')
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
        """returns a set of all out-edges of the graph"""
        s = set()
        for d in self.itervalues():
            s.update(d.itervalues())
        return s
    
    def in_edges(self, v):
        s = set()
        for w in self.inverse_graph[v]:
            s.update(self.inverse_graph[v][w])
        return s

    def out_edges(self, v):
        s = set()
        for w in self[v]:
            s.update(self[v][w])
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
        es = 0.0
        neighbors = self[v].keys()
        neighbors.extend(self.inverse_graph[v].keys())

        for w in neighbors:
            for u in neighbors:
                if self.get(v

        k = len(self[v]) + len(self.inverse_graph[v])
        try: 
            c = es / (k * (k-1))
        except ZeroDivisionError:
            c = es / (k * 1)
        print v, c
        return c

    def clustering_coefficient(self):
        local_cs = [self.cluster(v) for v in self.keys()]
        c = sum(local_cs) / len(local_cs)

        return c
        
class LoopError(Exception):
	
    def __init__(self, value):
		self.parameter = value
		
    def __str__(self):
        return repr(self.parameter)
 
        
def show_graph(g):
    for v in g.vertices():
        """if v.visited: 
            v.color = 'white'
        else:
            v.color = 'red'"""
        v.color='red'

    layout = GraphWorld.CircleLayout(g)
    gw = GraphWorld.GraphWorld(directed=True)
    gw.show_graph(g, layout)
    gw.mainloop()
        
if __name__ == '__main__':
    v = Vertex('v')
    w = Vertex('w')
    x = Vertex('x')
    e = DirectedEdge(v,w)
    e2 = DirectedEdge(x, w)
    e3 = DirectedEdge(x, v)
    dg = DirectedGraph([v, w, x],[e, e2, e3])
    print dg.clustering_coefficient()
    #show_graph(dg)
    
    
