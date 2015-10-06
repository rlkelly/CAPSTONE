from django.shortcuts import render


from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.template import RequestContext
from moody.forms import UserForm, UserProfileForm
from datetime import datetime
from sets import Set
import requests
import spotipy
import json
import random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import sys,os
import spotipy.util as util
from sets import Set
from random import shuffle
from urllib2 import urlopen

import pickle
from neo4jrestclient import client
db = client.GraphDatabase("http://54.84.132.154/db/data/", username="neo4j", password="plzwork2015")

bag_of_words = list(pickle.load(open("bag_of_words.pkl", "rb" )))

def genre(request, genre_slug):
    
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None


    context_dict['bag_of_words'] = bag_of_words

    if request.method == 'POST':
        query = request.POST.get('query')

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        q = 'MATCH (g:Genre {slug:\'%s\'})-[r]-p RETURN p ORDER BY toFloat(r.dist) ASC;' %(genre_slug)
        albums = [(each[0]['data']['name'],each[0]['data']['slug'],each[0]['data']['albumcover'])  for each in db.query(q)]

        q = 'MATCH (g:Genre {slug:\'%s\'}) RETURN g' %(genre_slug)
        genre = db.query(q)[0][0]['data']
        context_dict['genre_name'] = genre['name']
        context_dict['albums'] = albums

    except:
        pass

    if not context_dict['query']:
        context_dict['query'] = genre['name']

    if request.method == 'POST':
        tags = request.POST
        if len(tags)==1:
            albums, albumlist, query = suggest_artist(['random'])
        else:
            temp = dict(tags.lists())['tags']
            albums, albumlist, query = suggest_artist(temp)
        query = ', '.join(query)
        partial = 'https://embed.spotify.com/?uri=spotify:trackset:Playlist:'
        player = partial+albums

        return render(request, 'moody/search.html', {'query':query, 'albums': albums, 'player':player, 'bag_of_words':bag_of_words, 'albumlist':albumlist})

    return render(request, 'moody/genre.html', context_dict)

def word(request, word_slug):

    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None

    context_dict['bag_of_words'] = bag_of_words

    if request.method == 'POST':
        query = request.POST.get('query')

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        q = 'MATCH (g:Word {slug:\'%s\'})-[r]-p RETURN p ORDER BY toFloat(r.dist) ASC LIMIT 50;' %(word_slug)
        albums = [(each[0]['data']['name'],each[0]['data']['slug'],each[0]['data']['albumcover'])  for each in db.query(q)]

        q = 'MATCH (w:Word {name:\'%s\'}) RETURN w' %(word_slug)
        word = db.query(q)[0][0]['data']
        context_dict['word_name'] = word['name']
        context_dict['albums'] = albums

    except:
        pass

    if not context_dict['query']:
        context_dict['query'] = word['name']

    if request.method == 'POST':
        tags = request.POST
        if len(tags)==1:
            albums, albumlist, query = suggest_artist(['random'])
        else:
            temp = dict(tags.lists())['tags']
            albums, albumlist, query = suggest_artist(temp)
        query = ', '.join(query)
        partial = 'https://embed.spotify.com/?uri=spotify:trackset:Playlist:'
        player = partial+albums

        return render(request, 'moody/search.html', {'query':query, 'albums': albums, 'player':player, 'bag_of_words':bag_of_words, 'albumlist':albumlist})

    return render(request, 'moody/word.html', context_dict)

def album(request, album_name_slug):

    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None

    context_dict['bag_of_words'] = bag_of_words

    if request.method == 'POST':
        query = request.POST.get('query')

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query

    try:
        q = 'MATCH (p:Album {slug:\'%s\'}) RETURN p' %(album_name_slug)
        album = db.query(q)[0][0]['data']

        context_dict['album'] = album['name']
        context_dict['spotify'] = album['s_id']
        context_dict['image'] = album['albumcover']
        context_dict['slug'] = album['slug']

        q = 'MATCH (p:Album {slug: \'%s\'})-[r]-(b:Word) RETURN b ORDER BY toFloat(r.dist) ASC LIMIT 25' %(album_name_slug)
        words = [each[0]['data']['name'] for each in db.query(q)]
        context_dict['words'] = words


        q2 = 'MATCH (p:Album {name:\'%s\'})-[r]-(g:Genre) RETURN g' %(album['name'])
        context_dict['genre_tags'] = [(each[0]['data']['name'],each[0]['data']['slug']) for each in db.query(q2)]

        print 'bottleneck'

        q3 = """MATCH (p:Album {slug: \'%s\'})-[r]-(b:Word)-[r2]-(p2:Album) 
            WITH p2, COUNT(b) as similar
            MATCH p2-[r]-(w:Word)
            RETURN p2, (1.0*similar)/COUNT(w) as similarity ORDER BY similarity DESC LIMIT 4;""" %(album_name_slug)
        neigh = [each[0]['data'] for each in db.query(q3)]

        print 'time4'

        context_dict['neighbors'] = [(each['slug'],each['albumcover']) for each in neigh]

    except:
        pass

    if not context_dict['query']:
        context_dict['query'] = album['name']

    if request.method == 'POST':
        tags = request.POST
        if len(tags)==1:
            albums, albumlist, query = suggest_artist(['random'])
        else:
            temp = dict(tags.lists())['tags']
            albums, albumlist, query = suggest_artist(temp)
        query = ', '.join(query)
        partial = 'https://embed.spotify.com/?uri=spotify:trackset:Playlist:'
        player = partial+albums

        return render(request, 'moody/search.html', {'query':query, 'albums': albums, 'player':player, 'bag_of_words':bag_of_words, 'albumlist':albumlist})

    return render(request, 'moody/album.html', context_dict)

def index(request):
    q = "MATCH (p:Album) RETURN p"
    album_list = [each[0]['data'] for each in db.query(q)]
    # album_list = pickle.load(open("album_list.pkl", "rb"))
    shuffle(album_list)
    album_paginator = Paginator(album_list, 24) # Show 30 contacts per page
    page = request.GET.get('page')

    try:
        pagi = album_paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pagi = album_paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        pagi = album_paginator.page(paginator.num_pages)

    albums = [(a['albumcover'], a['artist'],a['slug']) for a in pagi]

    if request.method == 'POST':
        tags = request.POST
        if len(tags)==1:
            albums, albumlist, query = suggest_artist(['random'])
        else:
            temp = dict(tags.lists())['tags']
            albums, albumlist, query = suggest_artist(temp)
        query = ', '.join(query)
        partial = 'https://embed.spotify.com/?uri=spotify:trackset:Playlist:'
        player = partial+albums
        print query

        return render(request, 'moody/search.html', {'query':query, 'albums': albums, 'player':player, 'bag_of_words':bag_of_words, 'albumlist':albumlist})

    return render(request, 'moody/index2.html', {'albums': albums, 'pagi':pagi, 'bag_of_words':bag_of_words})

def search(request):

    q = 'MATCH (p:Album)-[r]-m RETURN m;'
    bag_of_words = [each[0]['data']['name'] for each in db.query(q)]
    context_dict['bag_of_words'] = list(Set(bag_of_words))

    album_list = Album.objects.order_by('?')
    page_list = []

    album_paginator = Paginator(album_list, 36) # Show 30 contacts per page

    return render(request, 'moody/search.html', {'albums': album})

def about(request):
    context_dict = {}

    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            art = form.save(commit=True)
            return index(request)
        else:
            print form.errors
    else:
        form = UserForm()

    context_dict['form'] = form

    context_dict['bag_of_words'] = bag_of_words

    return render(request, 'moody/about.html', context_dict)

def suggest_artist(request):
    request = map(lambda x: str(x).lower(), request)
    clone = request[:]
    genre_list = pickle.load(open("genre_list.pkl", "rb" ))
    results = None

    q = ""

    try:

        if request not in [['random'] , []]:
            for each in request[:]:
                if each in genre_list:
                    q += "MATCH p-[r]-(g:Genre {name:\'%s\'}) WITH p " %(each)
                    request.remove(each)
                if len(request) == 0:
                    q += ", rand() as r RETURN p ORDER BY r LIMIT 12;"
                    break

            print request
            while len(request) > 0:
                q += """MATCH (p:Album)-[r]-(w:Word {name:\'%s\'})
                RETURN p ORDER BY r.dist ASC LIMIT 12;""" %(request[0])
                request.remove(request[0])

            # else:
            #     q += """MATCH (p:Album)<-[r]-(tags)
            #     WHERE tags.name IN %s
            #     WITH p, COLLECT(tags) as tags, SUM(toFloat(r.dist)) as dist
            #     WHERE LENGTH(tags) = LENGTH(%s)
            #     RETURN p ORDER BY dist ASC LIMIT 12;""" %(request,request)

        print q

        results = db.query(q)
        print results

        if not results:
            q = """START t=node(*) 
                MATCH (a:Album)-[r]-(t) 
                RETURN a, rand() as r
                ORDER BY r
                LIMIT 12 """
            clone = ['random, query kinder please :-)']
            results = db.query(q)

    except:

        q = """START t=node(*) 
        MATCH (a:Album)-[r]-(t) 
        RETURN a, rand() as r
        ORDER BY r
        LIMIT 12 """
        clone = ['random, query kinder please :-)']
        results = db.query(q)

    tracklst = []
    albums = []

    for each in results:
        albums.append([each[0]['data']['name'],each[0]['data']['slug'],each[0]['data']['albumcover']])
        s_id =  each[0]['data']['s_id']
        url = 'http://api.spotify.com/v1/albums/%s/tracks' %(s_id[14:])
        a = urlopen(url).read()
        a = json.loads(a)['items']
        try:
            nums = random.sample(range(len(a)),2)
            tracklst.extend((a[nums[0]]['uri'][14:], a[nums[1]]['uri'][14:]))
        except:
            continue
    shuffle(tracklst)

    return (','.join(tracklst), albums, clone)
