
from bs4 import BeautifulSoup
from urllib2 import urlopen
from selenium import webdriver
import time

def djb_album_scrape(num_pages = 25):
    
    BASE_URL = "http://www.djbooth.net/index/albums/reviewed?p="
    linklist = []
    artistalbumlist = []
    driver = webdriver.Chrome()  # Optional argument, if not specified will search path.
    driver.get(BASE_URL);
    time.sleep(1) # Let the user actually see something!

    for i in range(1,num_pages):
           driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
           time.sleep(1)

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "lxml")
    left = soup.findAll('div', {'class':'index-features blocks'})

    links = [s['href'] for s in [s.findAll('a') for s in left][0]][::2]
    linklist.extend(links)

    artists = [s.text for s in [s.findAll('a') for s in left][0] if s.text != u'\n\n']
    artistalbumlist.extend(artists)

    return artistalbumlist, linklist

def djb_text_scrape(url):
    BASE_URL = 'http://www.djbooth.net'
    time.sleep(1)
    link = BASE_URL + url
    html = urlopen(link).read()
    soup = BeautifulSoup(html, "lxml")
    artist = soup.find('div', {'class':'artist-name'}).text.strip()
    album = soup.find('div', {'class':'song-name'}).text.strip()

    content = soup.findAll('div', {'class':'content'})
    text = [s.findAll(text=True) for s in content]
    text = ''.join([i for o in text for i in o]).encode('utf-8').strip()
    return artist, album, text, link

# links = djb_album_scrape(num_pages = 10)[1]

# for each in links[0:30:5]:
#     print djb_text_scrape(each)
