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
        if v != s: visited.add(v)

        # add its out vertices to the queue
        queue.extend(dg.out_vertices(v))
    return frozenset(visited)

def get_reachables(dg):
    """
    Find all the vertices that are reachable from each vertex v.
    """
    reachable = {}
    for v in dg.vertices():
        reachable[v] = bfs(v)

    return reachable

def same_reachables(v, reachables):
    """
    blah
    """
    t = reachables.get(v, None)
    print t
    if len(t) == 0:
        return False
        
    for w in reachables[v]:
            s = reachables.get(w, None)
            if len(s) == 0:
                return False
            x = s.symmetric_difference(t)
            if x != set([v, w]):
                return False
    print 'returning true'
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
    dg = DirectedGraph([v,w,x],[e1, e2, e3])
    print has_knot(dg)
    
        
