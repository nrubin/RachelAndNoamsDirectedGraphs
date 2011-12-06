from BeautifulSoup import BeautifulSoup
import pickle
import os
import urllib2
from DirectedGraph import DirectedGraph, Arc, Vertex, LoopError
from DirectedGraphWorld import show_directed_graph


def get_urls_by_criteria(parent, url_cache=None, criteria=''):
    """Returns a list of URLS linked to from the given page"""
    
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent','Mozilla/5.0')]
    
    #catches invalid links
    try:
        if 'http' not in parent:
            infile = opener.open("http://en.wikipedia.org" + parent)
        else:
            infile = opener.open(parent)
    except:
        #print 'URL error at ' + parent
        return []
    page = infile.read()
 
    #catches pages that are unparsable b/c of unicode in text
    try:
        soup = BeautifulSoup(page)
    except:
        #print 'Soup error at ' + parent
        return []
        
    #catches pages that are not formatted according to the standard
    try:
        content_div = soup.find('div',{'class':'mw-content-ltr'})
        links = content_div.findAll('a')
    except:
        #print 'Content div error at ' + parent
        return []

    results = []
    for l in links:
        #catches the case where there's <a></a> without an href
        try: next_link = str(l['href'])
        except: continue
        
        #you've made it this far, so you're golden for good links!
        if url_cache and next_link in url_cache and \
            criteria in next_link and \
            'redlink' not in next_link and \
            'php' not in next_link and\
            'Portal' not in next_link:
            results.append(next_link)
        elif not url_cache and criteria in next_link and \
            'redlink' not in next_link and \
            'php' not in next_link and \
            'Portal' not in next_link:
            results.append(next_link)
        else:
            pass

    return results

def makeGraphFromUrls(index_url):
    """
    creates a graph from the wikipedia URLS listed in
    index_url. Returns the graph.
    """
    url_cache = get_urls_by_criteria(index_url)
    vertices = [Vertex(url) for url in url_cache]
    dg = DirectedGraph(vertices, [])
    url_dict={}
    for url in url_cache:
        url_dict[url] = get_urls_by_criteria(url, url_cache, criteria='wiki')
        for out in url_dict[url]:
            try:
                a = Arc(Vertex(url), Vertex(out))
                dg.add_arc(a)
            except LoopError:
                print 'Loop Error at ' + url
    return dg

def save_object_to_file(dg,file_name):
    """
    Saves a directed graph dg to the file f.
    """
    f = open(file_name,'wb')
    pickle.dump(dg,f)
    f.close()
    
def load_object_from_file(file_name):
    """
    loads a pickled graph from a file and returns it.
    """
    f = open(file_name,'rb')
    dg = pickle.load(f)
    return dg

def find_all_indices(root):
    results = []
    urls = get_urls_by_criteria(root)
    for url in urls:
        if 'page does not exist' not in url and \
        'redlink' not in url and \
        'php' not in url and \
        'Index' in url:
            results.append(url)
    return results
        
def parse_indices(name='indices'):
    root = 'http://en.wikipedia.org/wiki/Portal:Contents/Indexes'
    indices = find_all_indices(root)
    save_object_to_file(indices, name)

def push_to_github(filename):

    os.popen('git add ' + filename)
    os.popen('git commit -m "committing graph: ' + filename + '"')
    os.popen('git push origin master')

def pull_from_github():
    os.popen('git pull origin master')

def create_graphs():
    try: 
        indices = load_object_from_file('indices.txt')
    except:
        parse_indices()
        indices = load_object_from_file('indices.txt')

    for index in indices:
        filename = index[6:] + '_graph.txt'
        try: 
            f = load_object_from_file(filename)
            print "Loaded %s" %(filename)
            i += 1
        except IOError:
            dg = makeGraphFromUrls(index)
            save_object_to_file(dg, filename)
            print "Saved %s" %(filename)

        
        
create_graphs()

#~ index_url = 'http://en.wikipedia.org/wiki/Index_of_anatomy_articles'
#~ dg = makeGraphFromUrls(index_url)
#~ print dg
#~ show_directed_graph(dg)
#~ saveGraph(dg,'/home/nrubin/Dropbox/School/_Fall2011/Computational_Modeling/RachelAndNoamsDirectedGraphs/wiki_graph1.txt')
#~ dg2 = loadGraph('/home/nrubin/Dropbox/School/_Fall2011/Computational_Modeling/RachelAndNoamsDirectedGraphs/PickledAnatomy.txt')
#~ show_directed_graph(dg2)
#~ print dg2.has_knot()

#~ test_results = set()
#~ for key, value in url_dict.items():
    #~ for item in value:
        #~ test_results.add(item)
        #~ 
#~ print test_results
#~ print set(url_cache)

