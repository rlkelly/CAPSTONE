
from bs4 import BeautifulSoup
from urllib2 import urlopen

def hhdx_album_scrape(num_pages = 1, section_url = 'reviews/'):
    
    BASE_URL = "http://hiphopdx.com/"
    linklist = []
    artistalbumlist = []
        
    for page in range(1,num_pages+1):
    	
        url = BASE_URL + section_url+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        heads = soup.findAll('h3', {'itemprop':'name'})
        # links = [s.a for s in heads]
        # links.extend([s['href'] for s in links])
        info = [s.findAll('a') for s in heads]
        artistalbumlist.extend([s[0].contents for s in info])
        links = [s[0]['href'] for s in info]
        if set(links)<= set(linklist):
            return artistalbumlist,linklist
        linklist.extend(links)

    return artistalbumlist, linklist

def hhdx_text_scrape(url):
    try:
        BASE_URL = 'http://www.hiphopdx.com'
        link = BASE_URL+url
        html = urlopen(link).read()
        soup = BeautifulSoup(html, "lxml")
        info = soup.find('h1', {'class':'headline'}).contents[0].split('-')
        if len(info) == 1:
            info = info[0].split(u'\u2013')

        artist = ''.join(info[0:-1]).strip()
        album = ''.join(info[-1:]).strip()

        text = soup.findAll('div', {'itemprop':'articleBody'})
        text = [s.findAll(text=True) for s in text][0]
    except:
        return
    return artist, album, ''.join(text).strip(), link

# links = hhdx_album_scrape(num_pages = 1)[1]
#  # for each in links[0::4]:
# print hhdx_text_scrape(links[0])
