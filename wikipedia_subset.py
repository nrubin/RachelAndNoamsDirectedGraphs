import BeautifulSoup
import urllib
import urllister

def getUrls(url):
    """Returns a list of urls linked to from the given page"""
    sock = urllib.urlopen(url)
    parser = urllister.URLLister()
    parser.feed(sock.read())
    sock.close()
    parser.close()
    return parser.urls

def main():
    test_url = "http://en.wikipedia.org/wiki/Index_of_neurobiology_articles"
    for x in getUrls(test_url):
        print x
    #http://en.wikipedia.org/wiki/Category:Indexes_of_science_articles


if __name__== "__main__":
    main()
