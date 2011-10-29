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

if __name__== "__main__":
    unittest.main()
