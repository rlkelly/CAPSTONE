from urllib2 import urlopen
from bs4 import BeautifulSoup

def music_terms():
    link = 'http://www.naxos.com/education/glossary.asp'
    html = urlopen(link).read()
    soup = BeautifulSoup(html)
    print soup.find('table').findAll('a')


print music_terms()