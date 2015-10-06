
from bs4 import BeautifulSoup
from urllib2 import urlopen

def sput_album_scrape(num_pages = 1, section_url = 'staff/albums/'):
    
    BASE_URL = "http://www.sputnikmusic.com/reviews/"
    linklist = []
    artistalbumlist = []
        
    for page in range(1,num_pages+1):
    	
        url = BASE_URL + section_url+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        new = soup.findAll('td', {'class':'bestnewmusic'})
        links = [s.a for s in new]
        links2 = [s['href'] for s in links]
        if set(links2)<= set(linklist):
            return artistalbumlist,linklist

        linklist.extend(links2)
        artistalbumlist.extend([s.find(text=True) for s in links])
    return artistalbumlist, linklist

def sput_text_scrape(url):
    try:
        BASE_URL = 'http://www.sputnikmusic.com'
        link = BASE_URL+url
        html = urlopen(link).read()
        soup = BeautifulSoup(html, "lxml")

        [s.extract() for s in soup.findAll('script')]

        info = soup.find('h1').findAll(text=True)
        artist = unicode(info[0])
        album = unicode(info[-1])
        text = soup.findAll('div', {'id': 'leftColumn'})[0]
        text = ''.join(text.findAll(text=True))
        text = text.split('Tweet')[0]
    except:
        return

    return artist, album, text, link

# links = sput_album_scrape(num_pages = 2)[1]
# for each in links[0::4]:
# 	print sput_text_scrape(each)