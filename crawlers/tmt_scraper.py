
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time

def tmt_album_scrape(num_pages = 1):
    
    BASE_URL = "http://www.tinymixtapes.com/music-reviews"
    linklist = []
    artistalbumlist = []    

    for page in range(0,num_pages):
        url = BASE_URL + "?page=" + str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        main = soup.findAll('div', {'id':'archives'})
        linkage = [s.findAll('a') for s in main]
        links = [s['href'] for s in linkage[0]][::2]
        if set(links)<=set(linklist):
            return artistalbumlist,linklist
        linklist.extend(links)
        info = [s.findAll(text=True) for s in linkage[0]][::2]
    return artistalbumlist, linklist

def tmt_text_scrape(url):
    try:
        time.sleep(1)
        BASE_URL = "http://www.tinymixtapes.com"
        link = BASE_URL + url
        html = urlopen(link).read()
        soup = BeautifulSoup(html, "lxml")
        artist = soup.find('span',{'itemprop':'name'}).get_text().strip()
        album = soup.find('span', {'class': 'subtitle'}).get_text().strip()
        texts = soup.findAll('div', {'itemprop':'reviewBody'})
        text = [s.get_text().strip() for s in texts]
    except:
        return
    return artist, album, ' '.join(text), link


# links = tmt_album_scrape(num_pages=1)[1]

# for each in links[0::4]:
#     print each
#     print tmt_text_scrape(each)
