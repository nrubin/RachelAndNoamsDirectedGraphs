from multiprocessing import Pool
from Wikipedia_PullAndParse import load_object_from_file, save_object_to_file
class IndexResults():
    """The class basically just acts a container for data, to make it 
    easier to store data, and then access it later
    """
    def __init__(self,name, k, c, n_vs, n_es):
        self.name = name
        self.clustering = c
        self.has_knot = k
        self.vertices = n_vs
        self.edges = n_es

def MultiThreadit():
    resultDict = dict() #resulting super awesome dictionary
    
    def cb(IndexResults):
        """
        Puts the analysis result in the return dictionary
        """
        resultDict[IndexResults.name] = IndexResults 
                    
    indices = load_object_from_file('../Graphs/indices.txt')
    po = Pool() #pool of processes
    for index in indices: #each process takes a graph, asynchronously
        po.apply_async(calculate,(index,),callback=cb)
    po.close()
    po.join()
    print resultDict
    return resultDict

def calculate(index):
    """
    takes a pickled graph. If it's been analyzed,
    returns the result of the analysis. Otherwise, 
    it analyzes the graph for clustering, knots,
    number of vertices and number of edges
    """
    filename = '../Graphs/' + index[6:] + '_graph.txt'
    try:
        results = load_object_from_file('../Results/' + index[6:] + '_results.txt')
        print "Loaded %s" %(index[6:])
    except IOError:
        g = load_object_from_file(filename)
        results = analyze_graph(g,index[6:])
        save_object_to_file(results, '../Results/' + index[6:] + '_results.txt')
        print "Saved %s" %(index[6:])
    except:
		print 'Something bad happened....'
    return results
      
def analyze_graph(g,name):
    #do the analysis
    c = g.clustering_coefficient()
    k = g.has_knot() 
    n_vs = len(g.vertices())
    n_es = len(g.arcs())
    
    #create the object to hold analysis
    res = IndexResults(name, k, c, n_vs,n_es)
    return res
        
if __name__ == '__main__':
    MultiThreadit()
    

#callback
#



