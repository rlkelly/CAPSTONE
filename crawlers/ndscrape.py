from bs4 import BeautifulSoup
from urllib2 import urlopen

    

def needledropreviewlist(pages=2,ans=None,link=None):

    reviewlist = []

    url = 'http://www.theneedledrop.com/'
    reviewpage = 'articles/?offset=1439348763881&reversePaginate=true&category=Reviews'

    while pages != 0:

        html = urlopen(url+reviewpage).read()
        soup = BeautifulSoup(html, "lxml")
        reviews = soup.find("div", {"class": "blog-content"}).findAll('h1')
        links =  [links.a.contents[0] for links in reviews]
        reviewlist.extend(links)
        
        reviewpage = soup.find("div", {"class": "older"}).find_all('a', href=True)[0]['href']
        
        pages -= 1

    return reviewlist


print needledropreviewlist(5)
