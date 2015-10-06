
from bs4 import BeautifulSoup
from urllib2 import urlopen

def nrp_album_scrape(num_pages = 1, section_url = 'music/'):
    
    BASE_URL = "http://www.noripcord.com/reviews/"
    linklist = []
    artistalbumlist = []
        
    for page in range(0,num_pages):
    	
        url = BASE_URL + section_url+'?page='+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")
        contents = soup.find('div', {'id':'content'})

        others = contents.findAll('h2')
        links = [s.a['href'] for s in others]
        info = [s.a.findAll(text=True) for s in others]
        artistalbumlist.extend(info)
        if set(links)<= linklist:
            return artistalbumlist,linklist
        linklist.extend(links)

    return artistalbumlist, linklist

def nrp_text_scrape(url):
    try:
        BASE_URL = 'http://www.noripcord.com'
        link = BASE_URL+url
        html = urlopen(link).read()
        soup = BeautifulSoup(html, "lxml")
        artist = unicode(soup.find('h1').contents[0])
        album = unicode(soup.find('h1').find('em').contents[0])
        text = soup.findAll('p')
        text = [s.findAll(text=True) for s in text]
        if text == []:
        	span = soup.findAll('span', {'class':'submitted'})
        	[s.extract() for s in span]
        	text = soup.findAll('div', {'id':'content'})
        	text = ''.join([s.findAll(text=True) for s in text][0]).split('Insound')[1].split('Tweet')[0]
    except:
        return
    return artist,album, ''.join([item for sublist in text for item in sublist]), link

# a,b,c = nrp_text_scrape(links[0])

# print type(a)
# print type(b)
# print type(c)