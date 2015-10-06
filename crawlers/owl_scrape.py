from bs4 import BeautifulSoup
from urllib2 import urlopen
import numpy as np

def owlmag_album_scrape(num_pages = 1, section_url = 'category/album-reviews/page'):

    BASE_URL = "http://www.theowlmag.com/"

    albumartistslist = []
    linkslist = []

    for num in range(1,num_pages+1):

        html = urlopen(BASE_URL + section_url+str(num)).read()
        soup = BeautifulSoup(html, "lxml")

        links = soup.find("div", {"id": "main"})

        albums = links.find_all('h2')
        album = [meta.contents[0] for meta in albums]
        metadata = [s.contents[0] for s in album]

        link = [s['href'] for s in album]

        for each in metadata:
            each = each.replace(u"\u2018", "").replace(u"\u2033", "").replace(u"\u201c","").replace(u"\u201d", "")
            each = each.split(' by ')
            album, artist = each[0], each[1:]
            albumartistslist.append((artist, album))
        if set(links)<= linkslist:
            return albumartistslist,linkslist

        linkslist.extend(link)

    return albumartistslist, linkslist

def owlmag_text_scrape(url):
    try:
        link = 'http://www.theowlmag.com/'
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        text = soup.findAll('p')
        final = [t.findAll(text=True) for t in text]
        title = soup.find('h1', {'class':'entry-title'})
        album, artist = title.text.replace(u"\u2018", "").replace(u"\u2033", "").replace(u"\u201c","").replace(u"\u201d", "").split(' by ')
        s = ""
        for each in np.array(final[2:-1]).flatten():
            s += ''.join(each).encode('utf-8')
    except:
        return
    return artist, album, ''.join([i for i in s if ord(i)<128]), url

#temp = owlmag_review_text('http://www.theowlmag.com/album-reviews/currents-by-tame-impala/')
