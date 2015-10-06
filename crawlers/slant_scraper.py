
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time

def slant_album_scrape(num_pages = 2):
    
    BASE_URL = "http://www.slantmagazine.com/music/P"
    linklist = []
    artistalbumlist = []
        
    for page in range(0,num_pages):
        try:
        	
            url = BASE_URL + str(page*17)
            html = urlopen(url).read()
            soup = BeautifulSoup(html, "lxml")

            heads = soup.findAll('div', {'class':'span8 noLeftPad'})
            names = [s.find('strong') for s in heads]
            artists = [s.contents[0] for s in names]
            albums = [s.findAll('h7') for s in heads]
            #albumtitles = [s.a.text for s in albums[0]]
            links = [s.a['href'] for s in albums[0]]
            if set(links) <= set(linklist):
                return artistalbumlist,linklist

            linklist.extend(links)
            artistalbumlist.extend(zip(artists, albumtitles))

        except:
            continue

    return artistalbumlist, linklist

def slant_text_scrape(url):
    try:
        time.sleep(1)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        artist = soup.find('h8').text
        album = soup.find('h7').text

        text = soup.find('div', {'class':'reviewContent'}).get_text()
        # text = [s.findAll(text=True) for s in text if s]
        # text = ''.join([''.join(s) for s in text if s])
        text = ''.join(text).strip()
    except:
        return

    return artist, album, text, url

# links = slant_album_scrape()[1]
# for each in links[0::4]:
#     print each
#     print slant_text_scrape(each)
