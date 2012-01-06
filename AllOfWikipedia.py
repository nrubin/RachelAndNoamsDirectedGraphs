import matplotlib.pyplot as pyplot
import Pmf
import Cdf
import MySQLdb
import math
import numpy
from DirectedGraph import Vertex, Arc, DirectedGraph
import DirectedGraphWorld

def GetData():
    db=MySQLdb.connect(host='mysql.coryis.me' ,user='reptar', passwd="sweetness",db="cory_main")
    c=db.cursor()
    query = 'SELECT COUNT(*) FROM pagelinks GROUP BY pl_from'
    c.execute(query)
    data = c.fetchall()
    return data

def CleanData(data):
    clean_data = []
    for item in data:
        clean_data.append(float(item[0]))
    return clean_data
    
def PlotData(data):
    pmf = Cdf.MakeCdfFromList(data)
    xs, ys = pmf.Render()
    #~ xs_log = []
    #~ ys_log = []
    #~ for x in xs:
        #~ if x <= 0:
            #~ xs_log.append(.00001)
        #~ else:
            #~ xs_log.append(math.log(x))
    #~ for y in ys:
        #~ if y <= 0:
            #~ ys_log.append(.00001)
        #~ else:
            #~ ys_log.append(math.log(y))
    #~ coefs = numpy.lib.polyfit(xs_log, ys_log, 1)
    #~ fit_y = numpy.lib.polyval(coefs, xs_log)
    #~ fit_y_log = [math.exp(1) ** f for f in fit_y]
    pyplot.plot(xs, ys, 'o')
    #~ pyplot.plot(xs, fit_y_log,'r--',linewidth=4)
    #~ pyplot.xscale('log')
    #~ pyplot.yscale('log')
    pyplot.ylabel('CDF(k)',fontsize=25)
    pyplot.xlabel('k',fontsize=25)
    pyplot.show()
    
def GetDataForGraphs():
    db=MySQLdb.connect(host='mysql.coryis.me' ,user='reptar', passwd="sweetness",db="cory_main")
    c=db.cursor()
    query = 'SELECT page.page_title, pagelinks.pl_title FROM pagelinks JOIN page ON pagelinks.pl_from = page.page_id'
    c.execute(query)
    data = c.fetchall()
    return data
    
def GetVertices(GraphData):
    names = []
    vertices = []
    for item in GraphData:
        names.append(item[0])
        names.append(item[1])
    for n in set(names):
        vertices.append(Vertex(n))
    return list(vertices)
    
def MakeArcs(GraphData):
    arcs = []
    for t in GraphData:
        if t[0] == t[1]:
            continue
        arcs.append(Arc(Vertex(t[0]),Vertex(t[1])))
    return arcs
    
def MakeGraph(GraphData):
    dg = DirectedGraph(GetVertices(GraphData),MakeArcs(GraphData))
    return dg

if __name__ == '__main__':
    #~ PlotData(CleanData(GetData()))
    dg = MakeGraph(GetDataForGraphs())
    print len(dg.vertices()), 'Vertices'
    print dg.has_knot()
