
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time

def bpm_album_scrape(num_pages = 2, section_url = 'reviews/page/'):
    
    BASE_URL = "http://beatsperminute.com/"
    linklist = []
    artistalbumlist = []
        
    for page in range(1,num_pages+1):
    	
        url = BASE_URL + section_url+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        heads = soup.findAll('div', {'class':'album_item'})

        info = [s.findAll('a') for s in heads]
        meta = [s.p.a.contents[0].split(' Review: ')[1].split(u'\u2013 ') for s in heads]
        artistalbumlist.extend(meta)
        links = [s[0]['href'] for s in info]
        if set(links) <= linklist:
            return artistalbumlist,linklist
        else:
            linklist.extend(links)

    return artistalbumlist, linklist

def bpm_text_scrape(url):
    try:
        time.sleep(1)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        artist = soup.findAll('h1')[1].text
        if artist == '':
            artist = soup.findAll('h2')[0].text
            album = soup.findAll('h3')[0].text
        else:
            album = soup.find('h2').text

        text = soup.findAll('p')
        text = [s.findAll(text=True) for s in text if s]
        text = ''.join([''.join(s) for s in text if s])
    except:
        return

    return artist, album, text, url

# print bpm_text_scrape('http://beatsperminute.com/reviews/album-review-rocketnumbernine-meyouweyou/')

# print bpm_album_scrape(num_pages = 1)

# # for each in links[0:4:4]:
# #     print bpm_text_scrape(each)
