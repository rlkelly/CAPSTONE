from urllib2 import urlopen
from bs4 import BeautifulSoup

def lookup_ud(word):
    link = 'http://www.urbandictionary.com/define.php?term=' + word
    html = urlopen(link).read()
    soup = BeautifulSoup(html)
    if soup.find('a', {'class':'word'}):
        synonyms = soup.findAll('ul', {'class':'tags no-bullet'})
        synonyms = [word.text.split('\n') for word in synonyms]
        try:
            return [word for word in synonyms[0] if len(word)>1]
        except:
            return synonyms
    else:
        return "NOT FOUND"


def lookup_dict(word):
    link = 'http://dictionary.reference.com/browse/' + word
    try:
        html = urlopen(link).read()
        soup = BeautifulSoup(html)
        print soup
        word = soup.find('h1', {'class':'head-entry'}).text
        return word
    except:
        return "NOT FOUND"


def thesaurus(word):
    link = 'http://www.thesaurus.com/browse/'+word
    html = urlopen(link).read()
    soup = BeautifulSoup(html)
    soup2 = soup.findAll('li')
    words = [word.findAll('strong', {'class': 'ttl'}) for word in soup2]
    idea = [item for sublist in words for item in sublist]
    return soup

print map(lambda x: lookup_ud(x), ['ass'])
