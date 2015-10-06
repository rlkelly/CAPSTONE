from neo4jrestclient import client
from json import loads

db = client.GraphDatabase("http://localhost:7474", username="neo4j", password="inside")

from urllib2 import urlopen
a = [u'war', u'pig']
a = map(lambda x: str(x), a)
print a

q = """MATCH (album:Album)-[r]-(tags)
WHERE tags.name IN %s
WITH album, COLLECT(tags) as tags, SUM(r.weight) as weight
WHERE LENGTH(tags) = LENGTH(%s)
RETURN album ORDER BY weight ASC LIMIT 10;""" %(a, a)

results = db.query(q)
print results

tracklst = []

for each in results:
    s_id =  each[0]['data']['s_id']
    url = 'http://api.spotify.com/v1/albums/%s/tracks?limit=2' %(s_id[14:])
    a = urlopen(url).read()
    a = loads(a)
    tracklst.extend((a['items'][0]['uri'], a['items'][1]['uri']))

print ','.join(tracklst)



