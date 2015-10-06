from bs4 import BeautifulSoup
from urllib2 import urlopen

def syff_album_scrape(num_pages = 5, section_url = 'album-reviews/'):
    
    BASE_URL = "http://www.syffal.com/"
    linklist = []
    artistalbumlist = []
        
    url = BASE_URL + section_url
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    #FEATURED REVIEW
    feat = soup.find("div", {"class": "albumReviewFeatureContent"})
    feat2 = soup.find("div", {"class": "albumReviewFeatureImage"})
    feature = feat.h2.contents[0], feat.h3.contents[0], feat2.a['href']

    #TOP REVIEWS
    land2 = soup.find("div", {"class": "landingTwo"})
    land2links = [c['href'] for c in land2.find_all('a')]
    temp = [c.find('img') for c in land2.find_all('a')]
    artistalbumdata1 = [a.get('title', '') for a in temp]

    #SECOND ROW REVIEWS
    land3 = soup.find("div", {"class": "landingThree"})
    land3links = [c['href'] for c in land3.find_all('a')]
    temp = [c.find('img') for c in land3.find_all('a')]
    artistalbumdata2 = [a.get('title', '') for a in temp]

    #SECONDARY CONTENT
    secondary = soup.find_all("div", {"class": "landingSecondaryContent"})
    secondarylinks = [c.h3 for c in secondary]
    links = [c.find('a')['href'] for c in secondarylinks]
    artistsalbums2n = [c.find('a').contents for c in secondarylinks]

    linklist.extend(feature)
    linklist.extend(land2links)
    linklist.extend(land3links)
    linklist.extend(links)

    def archives(num_pages = 5):
        url = 'http://www.syffal.com/album-reviews/archive?page='
        lst = []
        for each in range(1,num_pages+1):
            url2 = url + str(each)
            html = urlopen(url2).read()
            soup = BeautifulSoup(html, "lxml")

            archive = soup.find_all("div", {"class": "featureTitle"})
            links = [c.h3.a['href'] for c in archive]
            metainfo = [c.h3.a.contents for c in archive]
            lst.extend(links)

        return lst

    linklist.extend(archives())
    
    return linklist

def syff_text_scrape(link):
    url = 'http://www.syffal.com' + link
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")
    top = soup.find('div', {'class':'region region-title'})
    artist = top.find('h1').text
    album = top.find('h2').text
    body = soup.find('div', {'class':'albumReviewBody'}).text

    return artist, album, ''.join([ch for ch in body.encode('utf-8') if ord(ch)<128]), url


