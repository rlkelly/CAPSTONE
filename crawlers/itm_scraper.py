from bs4 import BeautifulSoup
from urllib2 import urlopen

def itm_album_scrape(num_pages = 2, section_url = 'music/'):
    
    BASE_URL = "http://www.inthemix.com.au/"
    linklist = []
    artistalbumlist = []
        
    for page in range(1,num_pages+1):
    	
        url = BASE_URL + section_url+'page-'+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        
        if page == 1:
            top = soup.find('div',{'id':'lead-heading'}).a
            artistalbumlist.extend([top.contents])
            linklist.append(top['href'])

        others = soup.findAll('h3')
        links = [s.a['href'] for s in others]
        albums = [s.a.text for s in others]
        artistalbumlist.extend([albums])
        links = links[:-1]
        if set(links) <= set(linklist):
            return artistalbumlist, linklist
        linklist.extend(links)

    return artistalbumlist, linklist

def itm_text_scrape(url):
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        text = soup.find("div", {"itemprop": "articleBody"})
        text = text.find_all(text=True)
        title = soup.title.contents[0]
        try:
            artist, album = title.split(' - ')
        except ValueError:
            try:
                artist, album = title.split(u'\u2013')
            except ValueError:
                artist, album = title.split(": ")
    except:
        print 'exception'
        return
    return artist, album, ' '.join(text), url

# print itm_text_scrape('http://www.inthemix.com.au/music/54791/Fabric_67_Zip')

# # print itm_album_scrape(num_pages=2)
# # for each in links[1][0:20:5]:
# # 	print cos_text_scrape(each)
