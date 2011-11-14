from DirectedGraph import DirectedGraph, DirectedVertex, DirectedEdge
from knots import Knots

import unittest

class TestKnots(unittest.TestCase):
    def setUp(self):
        self.v = DirectedVertex('v')
        self.w = DirectedVertex('w')
        self.x = DirectedVertex('x')
        self.e1 = DirectedEdge(self.v, self.w)
        self.e2 = DirectedEdge(self.w, self.x)
        self.e3 = DirectedEdge(self.x, self.v)
        
        self.dg = DirectedGraph([self.v, self.w, self.x], 
            [self.e1, self.e2, self.e3])
        
    def test_positive(self):
        
        #triangular knot
        self.assertEqual(self.dg.has_knot(), True)
  
        #triangular knot w/ an edge into it
        self.a = DirectedVertex('a')
        self.dg.add_vertex(self.a)
        self.Kanye = DirectedEdge(self.a,self.v)
        self.dg.add_edge(self.Kanye)
        self.assertEqual(self.dg.has_knot(),True)
    
    def test_ngon_with_chord(self):
        v1 = DirectedVertex('v1')
        v2 = DirectedVertex('v2')
        v3 = DirectedVertex('v3')
        v4 = DirectedVertex('v4')
        v5 = DirectedVertex('v5')
        e1 = DirectedEdge(v2,v1)
        e2 = DirectedEdge(v3,v2)
        e3 = DirectedEdge(v3,v4)
        e4 = DirectedEdge(v4,v5)
        e5 = DirectedEdge(v5,v1)
        
        ngon = DirectedGraph([v1,v2,v3,v4,v5],
            [e1,e2,e3,e4,e5])
        
        self.assertFalse(ngon.has_knot())
        
        chord = DirectedEdge(v1,v4)
        ngon.add_edge(chord)

        self.assertTrue(ngon.has_knot())
        
     
        
        
        
        
if __name__ == '__main__':
    unittest.main()
