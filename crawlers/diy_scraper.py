
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time

def diy_album_scrape(num_pages = 1):
    
    BASE_URL = "http://diymag.com/reviews/album"
    linklist = []
    artistalbumlist = []    

    for page in range(1,num_pages+1):
        url = BASE_URL + "/page-" + str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        main = soup.findAll('h3', {'class':'h-headline'})
        names = [s.a.text for s in main]
        artistalbumlist.extend(names)
        links = [s.a['href'] for s in main]
        if set(links) <= linklist:
            return artistalbumlist, linklist
        linklist.extend(links)
    return artistalbumlist, linklist

def diy_text_scrape(url):
    try:
        time.sleep(1)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        info = soup.find('span',{'class':'h-headline__main'}).get_text().strip()
        info = info.rsplit(' - ', 1)
        artist = info[0]
        album = info[1]

        tagline = soup.find('p', {'class':'h-standfirst'}).get_text().strip()
        text1 = soup.findAll('div', {'class':'col m-4 l-8 block--article__text intro'})
        text1 = [s.findAll(text=True) for s in text1][0]
        text2 = soup.findAll('div', {'class':'col m-8 l-8 block--article__text'})

        if text2 != []:
            text2 = [s.findAll(text=True) for s in text2][0]
            text2 = ''.join(text2).strip()
            text = tagline + ''.join(text1).strip() + text2
        else:
            text = tagline + ''.join(text1).strip()
    except:
        return

    return artist, album, text, url

# links = diy_album_scrape(num_pages=4)[1]
# for each in links[0::4]:
#     print diy_text_scrape(each)
