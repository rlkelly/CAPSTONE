
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time

def ap_album_scrape(num_pages = 1):
    
    BASE_URL = "http://www.absolutepunk.net/forumdisplay.php?f=166"
    linklist = []
    artistalbumlist = []    

    for page in range(1,num_pages+1):
        url = BASE_URL + "&page=%i&order=desc" %(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        tds = soup.findAll('table', {'class':'tborder'})
        trs = [s.findAll('a') for s in tds][0]
        links = [s['href'] for s in trs]
        artistalbumlist.extend([s for s in [s.text for s in trs] if s])
        if set(links) <= set(linklist):
            print 'set-finish'
            return artistalbumlist, linklist

        linklist.extend(links[::2])

    return artistalbumlist, linklist

def ap_text_scrape(url):
    try:
        time.sleep(1)
        BASE_URL = "http://www.absolutepunk.net/"
        link = BASE_URL+url
        html = urlopen(link).read()
        soup = BeautifulSoup(html, "lxml")
        info = soup.find('title').text.split('- Album')[0].rsplit(' - ', 1)
        artist = info[0]
        album = info[1]
        texts = soup.findAll('td', {'class':'alt1 big jt-content'})
        text = ''.join([s.findAll(text=True) for s in texts][1])
    except:
        return

    return artist, album, text, link


# links = ap_album_scrape(num_pages=2)[1]

# for each in links[0::4]:
#     print each
#     print ap_text_scrape(each)

