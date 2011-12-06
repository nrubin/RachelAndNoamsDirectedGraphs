from BeautifulSoup import BeautifulSoup
import pickle
import os
import urllib2
from DirectedGraph import DirectedGraph, Arc, Vertex, LoopError
from DirectedGraphWorld import show_directed_graph

def getUrls(url):
    """Returns a list of URLS linked to from the given page"""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0')]
    try:
        infile = opener.open(url)
    except:
        print 'URL error at ' + url
        return []
    page = infile.read()
    try:
        soup = BeautifulSoup(page)
    except:
        print 'Soup error at ' + url
    content_div = soup.find('div',{'class':'mw-content-ltr'})
    try:
        links = content_div.findAll('a')
        results = [str(l['href']) for l in links if 'wiki' in str(l['href'])]
    except:
        print 'Content div error at ' + url
        results = []
    return results

def getLimitedUrls(parent, url_cache):
    """Returns a list of URLS linked to from the given page"""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0')]
    try:
        infile = opener.open("http://en.wikipedia.org" + parent)
    except:
        print 'URL error at ' + parent
        return []
    page = infile.read()
    try:
        soup = BeautifulSoup(page)
    except:
        print 'Soup error at ' + parent
    try:
        content_div = soup.find('div',{'class':'mw-content-ltr'})
        links = content_div.findAll('a')
        results = [str(l['href']) for l in links if str(l['href']) in url_cache and 'wiki' in str(l['href'])]
    except:
        print 'Content div error at ' + parent
        results = []
    return results
    
def makeGraphFromUrls(index_url):
    """
    creates a graph from the wikipedia URLS listed in
    index_url. Returns the graph.
    """
    url_cache = getUrls(index_url)
    vertices = [Vertex(url) for url in url_cache]
    dg = DirectedGraph(vertices, [])
    url_dict={}
    for url in url_cache:
        url_dict[url] = getLimitedUrls(url, url_cache)
        for out in url_dict[url]:
            try:
                a = Arc(Vertex(url), Vertex(out))
                dg.add_arc(a)
            except LoopError:
                print 'Loop Error at ' + url
    return dg

def saveGraph(dg,file_location):
    """
    Saves a directed graph dg to the file f.
    """
    os.popen('rm ' + file_location)
    os.popen('touch ' + file_location)
    f = open(file_location,'wb')
    pickle.dump(dg,f)
    f.close()
    
def loadGraph(file_location):
    """
    loads a pickled graph from a file and returns it.
    """
    f = open(file_location,'rb')
    dg = pickle.load(f)
    return dg


#~ index_url = 'http://en.wikipedia.org/wiki/Index_of_neurobiology_articles'
#~ index_url = 'http://en.wikipedia.org/wiki/Index_of_anatomy_articles'
#~ dg = makeGraphFromUrls(index_url)
#~ print dg
#~ show_directed_graph(dg)
#~ saveGraph(dg,'/home/nrubin/Dropbox/School/_Fall2011/Computational_Modeling/RachelAndNoamsDirectedGraphs/wiki_graph1.txt')
dg2 = loadGraph('/home/nrubin/Dropbox/School/_Fall2011/Computational_Modeling/RachelAndNoamsDirectedGraphs/PickledAnatomy.txt')
show_directed_graph(dg2)
print dg2.has_knot()

#~ test_results = set()
#~ for key, value in url_dict.items():
    #~ for item in value:
        #~ test_results.add(item)
        #~ 
#~ print test_results
#~ print set(url_cache)
