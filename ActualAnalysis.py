from Wikipedia_PullAndParse import load_object_from_file, save_object_to_file
from multithread_analysis import *
import Cdf
import Pmf
import myplot
import numpy
import matplotlib.pyplot as pyplot
from DirectedGraph import *
import math
#clustering coeff. vs number of vertices

#proportion of knots

#total number of vertices
def total_number_of_vertices():
    #import indices.txt
    count = 0
    for key,val in megadict:
        count += val.n_vs
    return count
    indices = load_object_from_file('../Graphs/indices.txt')
    
    for index in indices: pass
    
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
    d, bin_size = BinnedKnots(zip(cs,k),10)
    x = []
    y = []
    for key, val in d.items():
        x.append(key)
        y.append(val)
    pyplot.bar(x, y,bin_size,facecolor='r')
    pyplot.xlabel('Clustering Coefficient')
    pyplot.ylabel('p')
    pyplot.title('Distribution of Proportion of Knots')
    pyplot.grid(True)
    pyplot.show()

def CompareToBA():
    """
    Let's generate some similar Barabasi Albert graphs and compare stuff
    
    Let's multithread this shit
    """
    from multiprocessing import Pool
    cs, k, vs, es = GetResultList()
    #~ dg = BADirectedGraph()
    avg_deg_data = [item[0] / float(item[1]) for item in zip(es,vs)]
    deg_vs = zip(vs,avg_deg_data)
    sim_cs = []
    sim_deg = []
    global count
    count = 0
    
    def cb(aTup):
        sim_cs.append(aTup[0])
        sim_deg.append(aTup[1]) 
        global count
        count += 1
        print count
        
    po = Pool()
    for pair in deg_vs[:-100]:
        po.apply_async(ParseGraph,(pair,),callback=cb)
        
    po.close()
    po.join()
    pyplot.figure(1)
    pyplot.plot(cs,sim_cs,'o')
    pyplot.xlabel('Real Clustering Coefficients')
    pyplot.ylabel('Model Clustering Coefficients')
    pyplot.title('Real vs. Modeled Clustering Coefficients')
    pyplot.savefig('ClusteringCompare', dpi=300,format='pdf')
    pyplot.figure(2)
    pyplot.plot(avg_deg_data,sim_deg,'o')
    pyplot.xlabel('Real Average Degree')
    pyplot.ylabel('Model Average Degree')
    pyplot.title('Real vs. Modeled Degrees')
    pyplot.savefig('DegreeCompare', dpi=300,format='pdf')
    pyplot.show()
    return
    
def ParseGraph(pair):
	try:
		deg = pair[0]
		num_vs = pair[1]
		dg = BADirectedGraph(int(math.floor(deg)))
		dg.build_graph(int(num_vs-deg))
		d = len(dg.edges())/float(len(dg.vertices()))
		c = dg.clustering_coefficient()
		print c, d
		return(c,d)
	except:
		return
    
def SomeDistributions(results):
    c = Cdf.MakeCdfFromList(vs)
    myplot.Cdf(c,show=True,complement=True,xscale='log')
    print max(vs)
    print min(vs)
    c2 = Cdf.MakeCdfFromList(cs)
    myplot.Cdf(c2,show=True)
    print sum(vs)
    


if __name__ == '__main__':
    CompareToBA()
