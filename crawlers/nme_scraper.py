
from bs4 import BeautifulSoup
from urllib2 import urlopen
import time

def nme_album_scrape(num_pages = 2, section_url = 'albums/page/'):
    
    BASE_URL = "http://www.nme.com/reviews/"
    linklist = []
    artistalbumlist = []
        
    for page in range(1,num_pages+1):
    	
        url = BASE_URL + section_url+str(page)
        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        heads = soup.findAll('h2', {'itemprop':'name'})
        links = [s.a['href'] for s in heads]
        if set(links) <= set(linklist):
            return artistalbumlist, linklist
        linklist.extend(links)
        artists = [s.a.contents[0] for s in heads]
        artists = [s.split(u' \u2013 ') if u'\u2013' in s else s.split(' - ') for s in artists]
        artistalbumlist.extend(artists)
    return artistalbumlist, linklist

def nme_text_scrape(url):
    try:
        time.sleep(1)
        BASE_URL = 'http://www.nme.com'
        link = BASE_URL + url
        html = urlopen(link).read()
        soup = BeautifulSoup(html, "lxml")
        info = soup.find('h1', {'itemprop':'name'}).text

        text = soup.findAll('span', {'class':'article_body'})
        text = [s.text for s in text]

        if "albums that may have" in info.lower():
        	week_dic = {}
        	bolds = soup.findAll('b')
        	artists = [s for s in bolds][::2]
        	if artists == []:
        		artists = [s for s in soup.findAll('strong') if s]
        		
        	for each in artists:
        		value = each.nextSibling.nextSibling
        		if value == u'\n':
        		    continue
        		else:
        		    week_dic[each.text] = each.nextSibling.nextSibling
        	return week_dic, 'albums', 'missed'

        if len(info.split(' - ')) > 1:
            artist = info.rsplit(' - ', 1)[0]
            album = info.rsplit(' - ', 1)[-1].strip().replace('\'', '')
        else:
            try:
                artist = info.rsplit(u'\u2013', 1)[0]
                album = info.rsplit(u'\u2013', 1)[1]
            except IndexError:
                artist = info.rsplit(": ")[0]
                album = info.rsplit(": ")[1]
    except:
        print 'exception'
        return   

    return artist, album, ''.join(text[0]).strip(), link 

# # #/reviews/various-artists/16177
# print nme_text_scrape('/reviews/robyn/16208')
