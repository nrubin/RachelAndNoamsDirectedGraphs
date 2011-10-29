import unittest
from DirectedGraph import DirectedGraph, DirectedEdge, Vertex

class TestDirectedGraph(unittest.TestCase):
    def test_reflexive(self):
        v = Vertex('v')
        w = Vertex('w')
        e = DirectedEdge(v, w)

        dg = DirectedGraph([v,w], [e])
        self.assertEqual(dg[v][w], e)
        self.assertEqual(dg[w], {})
        
        self.assertEqual(dg.inverse_graph[w][v], e)
        self.assertEqual(dg.inverse_graph[v], {})

if __name__== "__main__":
    unittest.main()
