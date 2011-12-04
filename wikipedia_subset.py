import BeautifulSoup
import urllib2
import urllister

    
def getPageSource(url):
    opener = urllib2.build_opner()
    opner.addheaders[('User-agent', 'Mozilla/5.0')]
    infile = opener.open(url)
    page = infile.read()

def main():
    test_url = "http://en.wikipedia.org/wiki/Index_of_neurobiology_articles"



if __name__== "__main__":
    main()
