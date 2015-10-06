from bs4 import BeautifulSoup
from urllib2 import urlopen

def cos_album_scrape(num_pages = 2, section_url = 'category/reviews/album-reviews/'):
    
    BASE_URL = "http://consequenceofsound.net/"
    linklist = []
    artistalbumlist = []
        
    for page in range(1,num_pages+1):

        url = BASE_URL + section_url+'page/'+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        meta = soup.find_all("div", {"class": "content"})
        wordage = [s.h1 for s in meta if s.h1 not in ([], None)]
        albumartist = [s.a.contents for s in wordage]
        link = [s.a['href'] for s in wordage]

        if set(link) <= set(linklist):
            return artistalbumlist, linklist

        linklist.extend(link)
        artistalbumlist.extend(albumartist)

    return artistalbumlist, linklist

def cos_text_scrape(url):
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        info = soup.find('h1', {'class':'post-title'})
        artist,album = info.contents[0].split(u'\u2013')
        text = soup.find_all("article", {"class": "post-content"})
        text = [t.findAll(text=True) for t in text][0]
        para = ''.join(text).encode('utf-8')
    except:
        return

    return artist, album, ''.join([i for i in para if ord(i)<128]).strip(), url

#url ="http://consequenceofsound.net/2015/08/album-review-royal-headache-high/"
# text = cos_album_scrape(num_pages = 5)[1]
# for each in text:
#     print each
#     print cos_review_text(each)

#print cos_review_text(url)

