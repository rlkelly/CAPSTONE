
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time

def iai_album_scrape(num_pages = 3, section_url = '/label/Album%20Review/'):
    
    BASE_URL = "http://www.itsallindie.com/search"
    linklist = []
    artistalbumlist = []
        
    for page in range(1,num_pages+1):
        if page == 1:
            url = 'http://www.itsallindie.com/search/label/Album%20Review?updated-max=2015-10-22T11:34:00%2B01:00&max-results=100&start=0&by-date=false'
        elif page == 2:
            url = "http://www.itsallindie.com/search/label/Album%20Review?updated-max=2014-06-17T11:26:00%2B01:00&max-results=100&start=22&by-date=false"
        else:
            url = 'http://www.itsallindie.com/search/label/Album%20Review?updated-max=2013-09-29T13:42:00%2B01:00&max-results=100&start=39&by-date=false'
    	
        url = BASE_URL + section_url+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        heads = soup.findAll('h3', {'class': 'post-title entry-title'})
        linklist.extend([s.a['href'] for s in heads])
        artistalbumlist.extend([s.a.contents for s in heads])

    return artistalbumlist, linklist

def iai_text_scrape(url):
    time.sleep(1)
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
 
    info = soup.find('h3').contents[0]
    aa = info.replace(u'\nALBUM REVIEW: ', "")
    aa = aa.replace('[ALBUM REVIEW] ', "").rsplit(' - ', 1)

    if len(aa) != 2:
        aa = aa[0][:-1]
        aa = aa.rsplit('\"')
        artist = aa[0]
        album = aa[1]
    else:
        artist = aa[0]
        album = aa[1]

    body = soup.findAll('div', {'class':'post-body entry-content'})    
    text = [s.findAll(text=True) for s in body][0]
    text = ''.join(text).replace("Follow/// Facebook", "").replace("Buy/// iTunes", "").strip()
    text = text.replace('Follow / [FACEBOOK]', "").replace('Listen / [YOUTUBE]', "").replace('Listen / [SOUNDCLOUD]', "").replace('Follow / [TWITTER]', "").replace('Listen / [WEBSITE]', "").strip()
    text = text.replace('[Facebook]', "").replace('[Twitter]',"").replace('[iTunes]', "")

    if "Album Review... " in artist:
        artist = artist.replace("Album Review... ", "").strip()

    if "Album Review:" in artist:
        artist = artist.replace("Album Review:", "").strip()

    if "EP Review" in artist:
        artist = artist.replace("EP Review", "").strip()

    return artist, album, text, url

# links = iai_album_scrape(num_pages = 2)[1]

# for each in links:
#     print each
#     print iai_text_scrape(each)
