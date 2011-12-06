from DirectedGraph import DirectedGraph, Vertex, Arc


import unittest

class TestKnots(unittest.TestCase):
    def setUp(self):
        self.v = Vertex('v')
        self.w = Vertex('w')
        self.x = Vertex('x')
        self.e1 = Arc(self.v, self.w)
        self.e2 = Arc(self.w, self.x)
        self.e3 = Arc(self.x, self.v)
        
        self.dg = DirectedGraph([self.v, self.w, self.x], 
            [self.e1, self.e2, self.e3])
        
    def test_positive(self):
        
        #triangular knot
        self.assertEqual(self.dg.has_knot(), True)
  
        #triangular knot w/ an edge into it
        self.a = Vertex('a')
        self.dg.add_vertex(self.a)
        self.Kanye = Arc(self.a,self.v)
        self.dg.add_edge(self.Kanye)
        self.assertTrue(self.dg.has_knot())
    
    def test_ngon_with_chord(self):
        v1 = Vertex('v1')
        v2 = Vertex('v2')
        v3 = Vertex('v3')
        v4 = Vertex('v4')
        v5 = Vertex('v5')
        e1 = Arc(v2,v1)
        e2 = Arc(v3,v2)
        e3 = Arc(v3,v4)
        e4 = Arc(v4,v5)
        e5 = Arc(v5,v1)
        
        ngon = DirectedGraph([v1,v2,v3,v4,v5],
            [e1,e2,e3,e4,e5])
        
        self.assertFalse(ngon.has_knot())
        
        chord = Arc(v1,v4)
        ngon.add_edge(chord)

        self.assertTrue(ngon.has_knot())
        
     
        
        
        
        
if __name__ == '__main__':
    unittest.main()
