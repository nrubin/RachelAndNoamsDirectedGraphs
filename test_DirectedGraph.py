import unittest
from DirectedGraph import DirectedGraph, DirectedEdge, Vertex

class TestDirectedGraph(unittest.TestCase):
    
    def test_graph_inverse_correspondance(self):
        """Does an edge FROM V to W get added to proper dictionaries?"""
        v = Vertex('v')
        w = Vertex('w')
        e = DirectedEdge(v, w)

        dg = DirectedGraph([v, w], [e])
        self.assertEqual(dg[v][w], e)
        self.assertEqual(dg[w], {})
        
        self.assertEqual(dg.inverse_graph[w][v], e)
        self.assertEqual(dg.inverse_graph[v], {})

    def test_remove_edge(self):
        v = Vertex('v')
        w = Vertex('w')
        e = DirectedEdge(v, w)

        dg = DirectedGraph([v, w], [e])

        dg.remove_edge(v, w)

        self.assertEqual(dg[v],{})
        self.assertEqual(dg.inverse_graph[w],{})
        self.assertEqual(dg[w], {})
        self.assertEqual(dg.inverse_graph[v], {})

    def test_in_out_degrees(self):
        
        v = Vertex('v')
        w = Vertex('w')
        x = Vertex('x')
        e = DirectedEdge(v, w)

        dg = DirectedGraph([v, w], [e])
        
        
        self.assertEqual(dg.out_degree(v),1)
        self.assertEqual(dg.in_degree(w),1)
        
        self.assertEqual(dg.out_degree(x),None)
        self.assertEqual(dg.in_degree(x),None)
        
        dg.remove_edge(v,w)
        
        self.assertEqual(dg.out_degree(v),0)
        self.assertEqual(dg.in_degree(w),0)
    
    def test_is_connected(self):
        v = Vertex('v')
        w = Vertex('w')
        e1 = DirectedEdge(v, w)
        e2 = DirectedEdge(w,v)

        dg = DirectedGraph([v, w], [e1,e2])
        self.assertEqual(dg.is_strongly_connected(),True)
        
        dg.remove_edge(w,v)
        
        self.assertEqual(dg.is_strongly_connected(),False)

    def test_complete(self):
        """a two-vertex complete graph is strongly connected."""
        v = Vertex('v')
        w = Vertex('w')
        
        dg = DirectedGraph([v,w])
        
        dg.complete()
        
        self.assertTrue(dg.is_strongly_connected())
        
    def test_is_complete(self):
        v = Vertex('v')
        w = Vertex('w')
        
        dg = DirectedGraph([v,w])
        
        dg.complete()
        
        self.assertTrue(dg.is_complete())
    
    def test_correct_inverse_graph(self):
        """checks that every out-edge in dg also exists as an in-edge
        in dg.inverse_graph"""
        v = Vertex('v')
        w = Vertex('w')
        e = DirectedEdge(v,w)
        
        dg = DirectedGraph([v,w],[e])
        
        #~ dg.complete()
        
        out_edges = set()
        in_edges = set()
        for v in dg.keys():
            for key,val in dg[v].items():
                out_edges.update(val)
        for w in dg.inverse_graph.keys():
            for key,val in dg.inverse_graph[w].items():
                in_edges.update(val)
    
        self.assertEqual(out_edges,in_edges)

if __name__== "__main__":
    unittest.main()
