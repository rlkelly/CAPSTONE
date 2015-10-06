from bs4 import BeautifulSoup
from urllib2 import urlopen

def pitchfork_album_scrape(num_pages = 6, section_url = 'reviews/albums/'):

    BASE_URL = "http://pitchfork.com/"

    albumartistslist = []
    linklist = []

    for num in range(1,num_pages+1):

        html = urlopen(BASE_URL + section_url+str(num)).read()
        soup = BeautifulSoup(html, "lxml")

        divs = soup.find("div", {"id": "main"})

        albums = divs.find_all('h2')
        album = [meta.contents[0] for meta in albums]

        artists = divs.find_all('h1')
        artist = [meta.contents[0] for meta in artists]

        linkages = divs.find_all('a')
        linkage = [b['href'] for b in linkages]
        links = linkage[:len(artist)]
        if set(links)<= set(linklist):
            return albumartistslist, linklist

        linklist.extend(links)
        albumartistslist.extend(zip(artist, album))

    return albumartistslist, linklist

def pitchfork_text_scrape(url):

    try:
        link = 'http://pitchfork.com'
        link = link + url
        html = urlopen(link).read()
        soup = BeautifulSoup(html, "lxml")
        body = soup.findAll('div', 'editorial')
        artist = soup.find('h1').text
        album = soup.find('h2').text
        text = ' '.join([t.findAll(text = True) for t in body][0])
    except:
        return
    return artist, album, text, link
