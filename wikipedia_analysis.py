from Wikpedia_PullAndParse import load_object_from_file, save_object_to_file
class IndexResults():
    """The class basically just acts a container for data, to make it 
    easier to store data, and then access it later
    """
    def __init__(self, k, c, n_vs):
        self.clustering = c
        self.has_knot = k
        self.vertices = n_vs
        
def analyze_graph(g):
    #do the analysis
    c = g.clustering_coefficient()
    k = g.has_knot()
    n_vs = g.vertices()
    
    #create the object to hold analysis
    res = IndexResults(k, c, n_vs)
    return res
    
def analyze_all():
    indices = load_object_from_file('indices.txt')
    
    for index in indices:
        filename = index[6:] + '_graph.txt'
        try:
            results = load_object_from_file(index[6:] + '_results.txt')
            print "Loaded %s" %(index[6:])
        except IOError:
            g = load_object_from_file(filename)
            results = analyze_graph(g)
            save_object_to_file(results, index[6:] + '_results.txt')
            print "Saved %s" %(index[6:])
        
if __name__ == '__main__':
    analyze_all()
    
