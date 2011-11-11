from DirectedGraph import DirectedGraph, DirectedVertex, DirectedEdge

class Knots():
    def __init__(self, dg):
        self.cache = {}
        self.dg = dg

        
    def bfs(self, s):
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

            
            for x in self.dg.out_vertices(v):
                
                #if its out vertices have been cached, update visited
                if x in self.cache.keys():
                    visited.update(self.cache[x])
                    visited.add(x)
                    
                #otherwise add its out vertices to the queue
                elif x not in self.cache.keys():
                    queue.append(x)
                    
        self.cache[s] = visited
        return visited

    def get_reachables(self):
        """
        Find all the vertices that are reachable from each vertex v.
        """
        for v in self.dg.vertices():
            self.cache[v] = self.bfs(v)


    def same_reachables(self, v):
        t = self.cache.get(v, None)

        if len(t) == 0:
            return False
            
        for w in self.cache[v]:
                s = self.cache.get(w, None)
                if len(s) == 0:
                    return False
                x = s.symmetric_difference(t)
                if x != set([v, w]):
                    return False

        return True

    def has_knot(self):
        self.get_reachables()
        for k, v in self.cache.items(): print k, v
        for v in self.dg.vertices():
            if self.same_reachables(v):
                return True
        return False
        
"""if __name__ == '__main__':
    v = DirectedVertex('v')
    w = DirectedVertex('w');
    x = DirectedVertex('x');
    e1 = DirectedEdge(v,w)
    e2 = DirectedEdge(w,x)
    e3 = DirectedEdge(x,v)
    dg = DirectedGraph([v,w,x],[e1, e2, e3])
    print has_knot(dg)"""
    
        
