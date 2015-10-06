
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time
def av_album_scrape(num_pages = 1):
    
    BASE_URL = "http://www.avclub.com/features/music-review/"
    linklist = []
    artistalbumlist = []    

    for page in range(1,num_pages+1):
        url = BASE_URL + "?page="+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        articles = soup.findAll('section', {'class':'article-list'})
        heads = [s.findAll('h1') for s in articles]
        artistalbumlist.extend([s.a.contents[0] for s in heads[0]])
        links = [s.a['href'] for s in heads[0]]
        if set(links)<= set(linklist):
            return artistalbumlist,linklist
        linklist.extend(links)

    return artistalbumlist, linklist

def av_text_scrape(url):
    try:
        time.sleep(1)
        BASE_URL = 'http://www.avclub.com'
        link = BASE_URL+url
        html = urlopen(link).read()
        soup = BeautifulSoup(html, "lxml")
        artist = soup.find('h3').find('span').find(text=True).strip()
        album = soup.find('div', {'class':'album'}).findAll(text=True)
        album = ''.join(album).rsplit('Album:\n')[1]
        text = soup.findAll('section', {'class':'article-text'})
        text = [s.get_text() for s in text][0].split('&amp;amp;amp;amp;')[0]
    except:
        return
    return artist, album, text, link


# links = av_album_scrape()[1]
# for each in links[0::4]:
#     print each
#     print av_text_scrape(each)
