from Wikipedia_PullAndParse import load_object_from_file, save_object_to_file
from multithread_analysis import *
import Cdf
import Pmf
import myplot
import numpy
import matplotlib.pyplot as pyplot
from DirectedGraph import *
import math
from multiprocessing import Pool
import StatTools

def GetResultList():
    """
    Returns a list of tuples containing the list of:
    clustering coefficients
    has_knot
    number of vertices
    number of edges
    """
    indices = load_object_from_file('../Graphs/indices.txt')
    cs = []
    k = []
    vs = []
    es = []
    for index in indices:
        try:
            result = load_object_from_file('../Results/' + index[6:] + '_results.txt')
            cs.append(result.clustering)
            k.append(result.has_knot)
            vs.append(result.vertices)
            es.append(result.edges)
        except:
            pass
    return cs, k, vs, es

def KnotProportion():
    cs, k, vs, es = GetResultList()
    count_true = 0
    for i in k:
        if i:
            count_true += 1
    return count_true / float(len(k))
    
def BinnedKnots(zipped,numBins):
    """
    Let's bin knots according to number of vertices, edges, or
    clustering
    @Args:
        A zipped list of the vs, es or cs and k
    """
    data, k = zip(*zipped)
    maxVal = max(data)
    minVal = min(data)
    binSize = (maxVal - minVal) / float(numBins)
    binDict = {}
    returnDict = {}
    bins = [(minVal,minVal+binSize)]
    n = 2
    while minVal + (n-1)*binSize < maxVal:
        bins.append((minVal+((n-1)*binSize),minVal+(n*binSize)))
        n += 1
    for item in zipped:
        for b in bins:
            if item[0] >= b[0] and item[0] <= b[1]:
                try:
                    knot_list = binDict[b]
                    #knot_list is (num_knots,total)
                except KeyError:
                    knot_list = None
                if knot_list and item[1]: #if the tuple is there and there's a knot
                    knot_list[0] += 1
                    knot_list[1] += 1
                elif knot_list and not item[1]: #if the tuple is there but there's no knot
                    knot_list[1] += 1
                elif item[1] and not knot_list: #if the tuple isn't there but there is a knot
                    binDict[b] = [1,1]
                else: #if there's no tuple or knot
                    binDict[b] = [0,1]
    for key,val in binDict.items():
        returnDict[key[0]] = val[0] / float(val[1]) #proportion of that bin that has a knot
    return returnDict, binSize

def ShowBinnedKnots():
    """
    Plots clustering coefficient vs. probability of a knot existing, 
    for the set of 558 graphs of wikipedia subsets
    """
    cs, k, vs, es = GetResultList()
    d, bin_size = BinnedKnots(zip(cs,k),10)
    x = []
    y = []
    for key, val in d.items():
        x.append(key)
        y.append(val)
    pyplot.bar(x, y,bin_size,facecolor='r')
    pyplot.xlabel('Clustering Coefficient')
    pyplot.ylabel('p(knot exists)')
    pyplot.grid(True)
    pyplot.show()
    pyplot.savefig('clustering_vs_knots')


def vertices_vs_pknot():
    """
    Plots the number of vertices vs probability of a  knot existing, 
    for the set  of 558 graphs of wikipedia subgraphs
    """
    cs, k, vs, es = GetResultList()
    d, bin_size = BinnedKnots(zip(vs, k), 25)
    x, y = [], []
    for key, val in d.items():
        x.append(key)
        y.append(val)
    d2, bin_size2 = StatTools.binData(vs,25)
    x2, y2 = [], []
    for key, val in d2.items():
        x2.append(key)
        y2.append(val)
    new_probs = [item[0] * item[1] for item in zip(y,y2)]        
    
    pyplot.bar(x, y, bin_size, facecolor='r')
    pyplot.xlabel("Number of vertices")
    pyplot.ylabel('p(knot exists)')
    pyplot.bar(x2,y2,bin_size2, facecolor='b')
    pyplot.bar(x2,new_probs,bin_size2, facecolor='g')
    pyplot.grid(True)
    pyplot.show()


    
    
def SomeDistributions(results):
    c = Cdf.MakeCdfFromList(vs)
    myplot.Cdf(c,show=True,complement=True,xscale='log')
    print max(vs)
    print min(vs)
    c2 = Cdf.MakeCdfFromList(cs)
    myplot.Cdf(c2,show=True)
    print sum(vs)
    

def compare_wikipedia_to_ba():
    """
    For wikipedia articles of at least 4000 vertices, builds a graph of
    k vs P(k), and finds line of best fit. Also builds this same graph
    for a Barabasi Albert graph on the same number of vertices.
    """
    indices = load_object_from_file('../Graphs/indices.txt')
    graphs = []
    for index in indices:
        try:
            results = load_object_from_file('../Results/' + index[6:] + '_results.txt')
            if results.vertices >= 3700:
                print index[6:]
                graph = load_object_from_file('../Graphs/' + index[6:] + '_graph.txt')
                graphs.append((index[6:], graph))
        except:
            pass
            
    for name, graph in graphs[:3]:
        #build list of in degree, out degree, total of each vertex
        ins, outs, totals = [], [], []
        for vertex in graph.vertices():
            deg_in = graph.in_degree(vertex)
            deg_out = graph.out_degree(vertex)
            deg_tot = deg_in + deg_out
            
            ins.append(deg_in)
            outs.append(deg_out)
            totals.append(deg_tot)
    
        #create a pmf of degrees
        pmf = Pmf.MakePmfFromList(outs)
        xs, ys = pmf.Render()
        
        #convert to log, so we can find line of best fit
        xs_log = []
        ys_log = []
        for x in xs:
            if x <= 0:
                xs_log.append(.00001)
            else:
                xs_log.append(math.log(x))
        for y in ys:
            if y <= 0:
                ys_log.append(.00001)
            else:
                ys_log.append(math.log(y))
        coefs = numpy.lib.polyfit(xs_log, ys_log, 1)
        fit_y = numpy.lib.polyval(coefs, xs_log)
        print coefs
        
        #transform fit line, to plot it on log-log scale
        fit_y_log = [math.exp(1) ** f for f in fit_y]
        pyplot.clf()
        pyplot.plot(xs, ys, 'o')
        pyplot.plot(xs, fit_y_log,'r--',linewidth=4)
        pyplot.xscale('log')
        pyplot.yscale('log')
        pyplot.xlabel('k')
        pyplot.ylabel('P(k)')

        #pyplot.show()
        title = 'out_degree_' + name
        pyplot.savefig(title)
        
        pyplot.clf()

        #BA graph w/ same # of vs; show that coefficient is the same
        vs = graph.vertices()
        bag = BADirectedGraph(5)
        bag.build_graph(len(vs)-5)
        ins, outs, totals = [], [], []
        for vertex in bag.vertices():
            deg_in = bag.in_degree(vertex)
            deg_out = bag.out_degree(vertex)
            deg_tot = deg_in + deg_out
            
            ins.append(deg_in)
            outs.append(deg_out)
            totals.append(deg_tot)
        pmf = Pmf.MakePmfFromList(outs)
        xs, ys = pmf.Render()
        
        #convert to log, so we can find line of best fit
        xs_log = []
        ys_log = []
        for x in xs:
            if x <= 0:
                xs_log.append(.00001)
            else:
                xs_log.append(math.log(x))
        for y in ys:
            if y <= 0:
                ys_log.append(.00001)
            else:
                ys_log.append(math.log(y))
        coefs = numpy.lib.polyfit(xs_log, ys_log, 1)
        fit_y = numpy.lib.polyval(coefs, xs_log)
        print coefs
        
        #transform fit line, to plot it on log-log scale
        fit_y_log = [math.exp(1) ** f for f in fit_y]
        
        pyplot.plot(xs, ys, 'o')
        pyplot.plot(xs, fit_y_log,'r--',linewidth=4)
        pyplot.xscale('log')
        pyplot.yscale('log')
        pyplot.xlabel('k')
        pyplot.ylabel('P(k)')

        pyplot.show()
        title = 'out_degree_BA_on_' + str(len(vs)) +'_vertices'
        pyplot.savefig(title)

        
def vertices_vs_has_knot():
    cs, ks, vs, es = GetResultList()
    xs, ys = [], []
    for c, k in zip(cs, ks):
        xs.append(c)
        if k: ys.append(1)
        else: ys.append(-1)
        
    pyplot.plot(xs, ys, 'o')
    pyplot.show()
        

if __name__ == '__main__':
    compare_wikipedia_to_ba()
    #ShowBinnedKnots()
    #vertices_vs_pknot()
    #vertices_vs_has_knot()
