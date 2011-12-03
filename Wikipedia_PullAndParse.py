from BeautifulSoup import BeautifulSoup
import pickle
import os
import urllib2
from DirectedGraph import DirectedGraph, Arc, Vertex
from DirectedGraphWorld import show_directed_graph

def getUrls(url):
    """Returns a list of URLS linked to from the given page"""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0')]
    infile = opener.open(url)
    page = infile.read()
    soup = BeautifulSoup(page)
    content_div = soup.find('div',{'class':'mw-content-ltr'})
    links = content_div.findAll('a')
    results = [str(l['href']) for l in links]
    return results

def getLimitedUrls(parent, url_cache):
    """Returns a list of URLS linked to from the given page"""
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0')]
    infile = opener.open("http://en.wikipedia.org" + url)
    page = infile.read()
    soup = BeautifulSoup(page)
    content_div = soup.find('div',{'class':'mw-content-ltr'})
    links = content_div.findAll('a')
    results = [str(l['href']) for l in links if str(l['href']) in url_cache]
    return results

def save_graph(dg,file_location):
    """
    Saves a directed graph dg to the file f.
    """
    os.popen('rm ' + file_location)
    os.popen('touch ' + file_location)
    f = open(file_location,'wb')
    pickle.dumps(dg,f,protocol = -1)
    f.close()

index_url = 'http://en.wikipedia.org/wiki/Index_of_neurobiology_articles'
url_cache = getUrls(index_url)

#graph stuff
vertices = [Vertex(url) for url in url_cache]
dg = DirectedGraph(vertices, [])
url_dict={}
print dg.vertices()
for url in url_cache:
    url_dict[url] = getLimitedUrls(url, url_cache)
    for out in url_dict[url]:
        a = Arc(Vertex(url), Vertex(out))
        dg.add_arc(a)
   
#~ dgw = DirectedGraphWorld()
#~ show_directed_graph(dg)
os.popen('touch ' + '/home/nrubin/Dropbox/School/_Fall2011/Computational_Modeling/RachelAndNoamsDirectedGraphs/wiki_graph1.txt')
save_graph(dg,'/home/nrubin/Dropbox/School/_Fall2011/Computational_Modeling/RachelAndNoamsDirectedGraphs/wiki_graph1.txt')

#~ test_results = set()
#~ for key, value in url_dict.items():
    #~ for item in value:
        #~ test_results.add(item)
        #~ 
#~ print test_results
#~ print set(url_cache)
