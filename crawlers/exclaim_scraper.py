
from bs4 import BeautifulSoup
from urllib2 import urlopen
import urllib2
import time

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
   'Accept-Encoding': 'none',
   'Accept-Language': 'en-US,en;q=0.8',
   'Connection': 'keep-alive'}

def exclaim_album_scrape(num_pages = 2, section_url = 'Album_EP/Page/'):
    
    BASE_URL = "http://exclaim.ca/music/Reviews/"
    linklist = []
    artistalbumlist = []
        
    for page in range(1,num_pages+1):
    	
        url = BASE_URL + section_url+str(page)
        req = urllib2.Request(url, headers=hdr)
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html, "lxml")

        heads = soup.findAll('h4')
        artists = [s.contents[0] for s in heads]
        albums = [s.contents[0].strip() for s in soup.findAll('span', {'class':'streamSingle-item-details'})]
        info = zip(artists, albums)
        artistalbumlist.extend(info)
        
        links = [s.findAll('a') for s in soup.findAll('ul', {'class':'streamSingle'})]
        links = [s['href'] for s in links[0] if s]
        if set(links)<= set(linklist):
            return artistalbumlist, linklist
        linklist.extend(links)

    return artistalbumlist, linklist

def exclaim_text_scrape(url):
    try:
        time.sleep(1)
        req = urllib2.Request(url, headers=hdr)
        html = urllib2.urlopen(req).read()
        soup = BeautifulSoup(html, "lxml")
        article = soup.find('div', {'class': 'article'})
        artist = article.find('h1').text
        album = article.find('h2').text

        [s.extract() for s in article.findAll('div')]
        [s.extract() for s in article.findAll('h1')]
        [s.extract() for s in article.findAll('h2')]
        
        text = ''.join(article.findAll(text = True))
    except:
        return

    return artist, album, text, url

print exclaim_album_scrape(num_pages=2)[1]

#links = exclaim_album_scrape(num_pages=2)[1]

# for each in links[0::4]:
#      print exclaim_text_scrape(each)
