from DirectedGraph import DirectedGraph, DirectedVertex, DirectedEdge

def bfs(s):
    """
    Breadth first search. Modified. Returns the set of vertices that
    are accessible by some path from s.

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
        visited.add(v)

        # add its out vertices to the queue
        queue.extend(dg.out_vertices(v))
    return visited

def get_reachables(dg):
    """
    Find all the vertices that are reachable from each vertex v.
    """
    reachable = {}
    for v in dg.vertices():
        reachable[v] = bfs(v)
    #~ print reachable
    return reachable

def same_reachables(v, reachables):
    """
    blah
    """
    for w in reachables[v]:
        if len(reachables[w]) > 1:
            inter = reachables[w].intersection(reachables[v])
            print inter
            if inter != reachables[v] or inter != reachables[w]:
                if inter != set():
                    return False
    #print reachables
    return True

def has_knot(dg):
    reachables = get_reachables(dg)
    for v in dg.vertices():
        print v
        if same_reachables(v, reachables):
            return True
    return False
    
if __name__ == '__main__':
    v = DirectedVertex('v')
    w = DirectedVertex('w');
    x = DirectedVertex('x');
    e1 = DirectedEdge(v,w)
    e2 = DirectedEdge(w,x)
    e3 = DirectedEdge(x,v)
    dg = DirectedGraph([v,w,x],[e1])
    print has_knot(dg)
    
        
