import pickle
from py2neo import Graph
from py2neo import Node, Relationship
import random
from py2neo import Graph
from py2neo.ext.ogm import Store
from slugify import slugify
import pandas as pd


from py2neo import authenticate, Graph

graph = Graph('http://neo4j:Zip88jobs@52.23.155.114/db/data/')
# print 'ufgh'
# alice = Node("Person", name="Alice")
# graph.create(alice)
# graph.push()

df = pickle.load(open('term_matrix.pkl', 'rb'))

graph.schema.create_uniqueness_constraint("Album", "slug")
# graph.schema.create_uniqueness_constraint("Word", "slug")
# graph.schema.create_uniqueness_constraint("Genre", "slug")

for i,r in df.iterrows():

    s_id = r['spotify_id']
    cover = r['albumcover']
    artist = r['artist_column']
    album = r['album_column']
    slug = r['slug_column']
    print [album]
    album = Node('Album', name = album, artist = artist, albumcover = cover, s_id = s_id, slug = slugify(slug))
    graph.create(album)
    graph.push()

    if pd.Series(r['genre_column']).any():
        for each in r['genre_column']:
            genre = graph.find_one('Genre', 'slug', slugify(each[0]))
            if not genre:
                genre = Node('Genre', name=each[0], slug=slugify(each[0]))
            rel = Relationship(album, 'Performs', genre, dist=each[1])
            graph.create(rel)
    for value in zip(r.index[5:],r[5:]):
        if value[1] != 1:
            word = graph.find_one('Word', 'slug', slugify(value[0]))
            if not word:
                word = Node('Word', name=value[0], slug=slugify(value[0]))
            rel = Relationship(word, 'Describes', album, dist=value[1])
            graph.create(rel)
