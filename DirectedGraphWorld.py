from Graph import Vertex, Edge, Graph
from RandomGraph import RandomGraph
from DirectedGraph import DirectedGraph,BA_smallworld
import math
import string
import random
from GraphWorld import GraphWorld, GraphCanvas, Layout, CircleLayout,RandomLayout

class DirectedGraphCanvas(GraphCanvas):
    def draw_edge(self, e):
        """Draw a directed edge as a line with an arrow"""
        v, w = e
        vx, vy = v.pos
        wx, wy = w.pos
        #~ r = 0.45
        #~ d = (wx-vx,wy-vy)
        #~ vshift = (vx + r*d[0], vy + r*d[1])
        #~ wshift = (wx + r*d[0], vy + r*d[1])
        y = math.fabs(vy) + math.fabs(wy)
        x = math.fabs(vx) + math.fabs(wx)
        theta = math.atan2(y, x)
        #~ if vx >= 0 and vy >= 0:
            #~ vshift = 
        
        wshift = (wx - .45 * math.cos(theta), wy - .45 * math.sin(theta))
        vshift = (vx - .45 * math.cos(theta), vy - .45 * math.sin(theta))

        tag = self.line([vshift, wshift], arrow="last", arrowshape="20 20 8")
        return tag


class DirectedGraphWorld(GraphWorld):
    
    #~ def __init__(self):  
        #~ GraphWorld.__init__(self)
        #~ self.setup()

    def setup(self):
        """Create the widgets."""
        self.ca_width = 400
        self.ca_height = 400
        xscale = self.ca_width / 20
        yscale = self.ca_height / 20

        # canvas
        self.col()

        self.canvas = self.widget(DirectedGraphCanvas, scale=[xscale, yscale],
                              width=self.ca_width, height=self.ca_height,
                              bg='white')
        
        # buttons
        self.row()
        self.bu(text='Clear', command=self.clear)
        self.bu(text='Quit', command=self.quit)
        self.endrow()
        
def show_graph(g):
    """
    Uses DirectedGraphWorld to show a DirectedGraph using Allen Downey's
    GraphWorld.
    """
    for v in g.vertices():
        """if v.visited: 
            v.color = 'white'
        else:
            v.color = 'red'"""
        v.color='red'

    layout = CircleLayout(g)
    gw = DirectedGraphWorld()
    gw.show_graph(g, layout)
    gw.mainloop()

def main(script, n='10', *args):

    #~ # create n Vertices
    #~ n = int(n)
    #~ labels = string.ascii_lowercase + string.ascii_uppercase
    #~ vs = [Vertex(c) for c in labels[:n]]
#~ 
    #~ # create a graph and a layout
    #~ rdg = DirectedRandomGraph(vs)
    #~ rdg.add_random_edges(p=.2)
    #~ print rdg.is_complete()
    
    #~ v = Vertex('v')
    #~ w = Vertex('w')
    #~ x = Vertex('x')
    #~ dg = DirectedGraph(vs)
    #~ dg.add_regular_edges(4)
    #~ dg.rewire(p=1)
#~ 
    #~ layout = CircleLayout(dg)
#~ 
    #~ # draw the graph
    #~ gw = DirectedGraphWorld()
    #~ gw.show_graph(dg, layout)
    #~ gw.mainloop()
    n, mo = 10, 2
    bag = BA_smallworld(mo)
    bag.build_graph(n)
    show_graph(bag)
    



if __name__ == '__main__':
    import sys
    main(*sys.argv)
