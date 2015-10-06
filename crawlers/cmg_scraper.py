from bs4 import BeautifulSoup
from urllib2 import urlopen

def cmg_album_scrape(num_pages = 2, section_url = 'records/'):
    
    BASE_URL = "http://cokemachineglow.com/"
    linklist = []
    artistalbumlist = []
        
    for page in range(1,num_pages+1):
    	
        url = BASE_URL + section_url+'?pg='+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        
        others = soup.findAll('h2')
        links = [s.a['href'] for s in others]
        albums = [s.a.text for s in others]
        artistalbumlist.extend(albums)
        if set(links)<=set(linklist):
            return artistalbumlist, linklist
        linklist.extend(links)

    return artistalbumlist, linklist

def cmg_text_scrape(url):
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        artist = unicode(soup.find('h1').contents[0])
        album = unicode(soup.find('h2').find('em').contents[0])
        text = soup.find('div', {'class':'articleborder'})
        text = text.findAll(text=True)
    except:
        return
    return artist,album, ''.join(text).strip(), url

# for each in cmg_album_scrape(1)[1]:
#     print cmg_text_scrape(each)
# links = cmg_album_scrape(num_pages=3)[1]
# for each in links[0:20:4]:
# 	print cos_text_scrape(each)