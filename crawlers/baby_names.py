from urllib2 import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.avss.ucsb.edu/NameGB.HTM').read()
soup = BeautifulSoup(html)
soup = soup.findAll('td')
table = [word.text for word in soup]
girls_names = table[1::7][1:]
boys_names =  table[5::7][1:]
girls_names = [name.lower() for name in girls_names]
boys_names = [name.lower() for name in boys_names]
boys_names[::-1]
