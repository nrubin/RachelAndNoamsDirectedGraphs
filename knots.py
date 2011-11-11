from DirectedGraph import DirectedGraph, DirectedVertex, DirectedEdge

class Knots():
    def __init__(self, dg):
        self._knot_cache = {}
        self.dg = dg

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

            
            for x in self.dg.out_vertices(v):
                
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
        #build the cache of which vertices are accessible from which
        for v in self.dg.vertices():
            self._knot_cache[v] = self._bfsknots(v)

        #searches for knot
        for v in self.dg.vertices():
            if self._knot_at_v(v):
                return True
        return False
        

    

