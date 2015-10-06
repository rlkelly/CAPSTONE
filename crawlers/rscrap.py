from bs4 import BeautifulSoup
from urllib2 import urlopen

#get links to all review pages from undertheradarmag

html = 'http://www.undertheradarmag.com/reviews/destroyer_poison_season/'

def utr_album_scrape(num_pages=10, section_url = 'category/music/'):
    BASE_URL = "http://www.undertheradarmag.com/reviews/"

    albumartistslist = []
    linklist = []

    for each in range(num_pages):

        html = urlopen(BASE_URL + section_url+'P'+str(each*10)).read()
        soup = BeautifulSoup(html, "lxml")
        head = soup.findAll("div", "headline")
        artist_list = [h3.a.contents[0] for h3 in head]
        album_list = [h4.i.a.contents[0] for h4 in head]
        category_links = [h3.a["href"] for h3 in head]
        albumartistslist.extend(zip(artist_list, album_list))
        links = category_links[0:len(artist_list)]
        
        if set(links)<= set(linklist):
            return albumartistslist, linklist

        linklist.extend(links)

    return albumartistslist, linklist


def utr_text_scrape(url):
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        artist = soup.find('h3').text
        album = soup.find('h4').text
        body = soup.findAll('p')
        review = [p.findAll(text=True) for p in body]
        #print [''.join(s.findAll(text=True))for s in body]
        text = ''.join([i for j in review for i in j]).split('Author rating')[0].split('BEGIN')[1]
    except:
        return
    return artist, album, text, url
# for each in utr_album_scraper(num_pages = 1)[1]:
#     print each
#     print utr_text_scrape(each)