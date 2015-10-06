
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time

def clash_album_scrape(num_pages = 2):
    
    BASE_URL = "http://www.clashmusic.com/reviews/album/"
    linklist = []
    artistalbumlist = []    

    for page in range(0,num_pages):
        url = BASE_URL + "?page="+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        top = soup.find('h2', {'class':'node__title node-title'}).extract()
        
        nodes = soup.findAll('h2', {'class':'node__title node-title'})
        artistalbumlist.extend([s.a.contents[0].rsplit(' - ', 1) for s in nodes])
        links = [s.a['href'] for s in nodes]
        if set(links) <= linklist:
            linklist.append(top.a['href'])
            artistalbumlist.extend([top.a.contents[0].rsplit(' - ', 1)])
            return artistalbumlist, linklist
        linklist.extend(links)
        
    linklist.append(top.a['href'])
    artistalbumlist.extend([top.a.contents[0].rsplit(' - ', 1)])

    return artistalbumlist, linklist

def clash_text_scrape(url):
    try:
        time.sleep(1)
        BASE_URL = 'http://www.clashmusic.com'
        link = BASE_URL+url
        html = urlopen(link).read()
        soup = BeautifulSoup(html, "lxml")
        title = soup.findAll('h2', {'class':'pane-title'})[-1].text
        try:
            artist,album = title.rsplit(' - ', 1)
        except ValueError:
            artist,album = title.rsplit(':', 1)

        tagline = soup.find('div', {'class': 'field-item even'}).contents[0]

        text = soup.findAll('div', {'class':'field-item even'})
        text = [s.findAll(text=True) for s in text if s]
        text = ''.join([''.join(s) for s in text if s]).split('Words: ')[0]
        text = ''.join(text).strip()
    except:
        return
    return artist, album, ''.join([tagline, text]), link

# for each in links[0::]:
#     print each
#     print clash_text_scrape(each)
