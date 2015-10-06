import pandas as pd
import numpy as np

from crawlers.ap_scraper import *
from crawlers.av_scraper import *
from crawlers.bpm_scraper import *
from crawlers.clash_scraper import *
from crawlers.cmg_scraper import *
from crawlers.cosscrape import *
from crawlers.diy_scraper import *
from crawlers.hhdx_scraper import *
from crawlers.exclaim_scraper import *
from crawlers.itm_scraper import *
from crawlers.nme_scraper import *
from crawlers.nrp_scraper import *
from crawlers.owl_scrape import *
from crawlers.pscrap import *
from crawlers.rscrap import *
from crawlers.slant_scraper import *
from crawlers.sput_scraper import *
from crawlers.tmt_scraper import *
from crawlers.syff_scrape import *

from pyechonest import config
from pyechonest import song
from pyechonest import artist
import spotipy
import time

import pickle
import string
from nltk.corpus import stopwords
from nltk import pos_tag
import time
import os
import re
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

#SCRAPING MUSIC BLOGS FOR REVIEW DATA
ap_info = ap_album_scrape(15)
ap_list = []
for each in ap_info[1]:
    ap_list.append(ap_text_scrape(each))

av_info = av_album_scrape(15)
av_list = []
for each in av_info[1]:
    av_list.append(av_text_scrape(each))

bpm_info = bpm_album_scrape(15)
bpm_list = []
for each in bpm_info[1]:
    bpm_list.append(bpm_text_scrape(each))

clash_info = clash_album_scrape(50)
clash_list = []
for each in clash_info[1]:
    clash_list.append(clash_text_scrape(each))

info = cmg_album_scrape(25)
cmg_list = []
for each in info[1]:
    cmg_list.append(cmg_text_scrape(each))

cos_info = cos_album_scrape(25)
cos_list = []
for each in cos_info[1]:
    cos_list.append(cos_text_scrape(each))

info = diy_album_scrape(35)
diy_list = []
for each in info[1]:
    try:
        diy_list.append(diy_text_scrape(each))
    except:
        print each

exclaim_info = exclaim_album_scrape(30)
exclaim_list = []
for each in exclaim_info[1]:
    exclaim_list.append(exclaim_text_scrape(each))

hhdx_info = hhdx_album_scrape(50)
hhdx_list = []
for each in hhdx_info[1]:
    hhdx_list.append(hhdx_text_scrape(each))

itm_info = itm_album_scrape(50)
itm_list = []
for each in itm_info[1]:
    try:
        itm_list.append(itm_text_scrape(each))
    except:
        print each

nme_info = nme_album_scrape(50)
nme_list = []
for each in nme_info[1]:
    try:
        nme_list.append(nme_text_scrape(each))
    except:
        print each

#SET DICTIONARY ASIDE FOR LATER

nme_dict_list = []
nme_df_list = []
for each in nme_list:
    try:
        if type(each[0]) == dict:
            nme_dict_list.append(each)
        else:
            nme_df_list.append(each)
    except:
        print each

nrp_info = nrp_album_scrape(50)
nrp_list = []
for each in nrp_info[1]:
    try:
        nrp_list.append(nrp_text_scrape(each))
    except:
        print each

owl_info = owlmag_album_scrape(30)
owl_list = []
for each in owl_info[1]:
    try:
        owl_list.append(owlmag_text_scrape(each))
    except:
        print each

pitc_info = pitchfork_album_scrape(100)
pitc_list = []
for each in pitc_info[1]:
    try:
        pitc_list.append(pitchfork_text_scrape(each))
    except:
        print each

utr_info = utr_album_scrape(30)
utr_list = []
for each in utr_info[1]:
    try:
        utr_list.append(utr_text_scrape(each))
    except:
        print each

slant_info = slant_album_scrape(30)
slant_list = []
for each in slant_info[1]:
    try:
        slant_list.append(slant_text_scrape(each))
    except:
        print each

sput_info = sput_album_scrape(30)
sput_list = []
for each in sput_info[1]:
    try:
        sput_list.append(sput_text_scrape(each))
    except:
        print each

tmt_info = tmt_album_scrape(30)
tmt_list = []
for each in tmt_info[1]:
    try:
        tmt_list.append(tmt_text_scrape(each))
    except:
        print each

syff_info = syff_album_scrape(40)
syff_list = []
for each in syff_info:
    ap_list.append(ap_text_scrape(each))

#COMBINE REVIEWS INTO DATAFRAME

avDf = pd.DataFrame(av_list)
avDf['site'] = 'AV.'
apDf = pd.DataFrame([rev for rev in ap_list if rev])
apDf['site'] = 'AP.'
bpmDf = pd.DataFrame(bpm_list)
bpmDf['site'] = 'BPM.'
clashDf = pd.DataFrame([rev for rev in clash_list if rev])
clashDf['site'] = 'CLA.'
cmgDf = pd.DataFrame([rev for rev in cmg_list if rev])
cmgDf['site'] = 'CMG.'
cosDf = pd.DataFrame([rev for rev in cos_list if rev])
cosDf['site'] = 'COS.'
diyDf = pd.DataFrame([rev for rev in diy_list if rev])
diyDf['site'] = 'DIY.'
exclaimDf = pd.DataFrame([rev for rev in exclaim_list if rev])
exclaimDf['site'] = 'EXC.'
hhdxDf = pd.DataFrame([rev for rev in hhdx_list if rev])
hhdxDf['site'] = 'HHD.'
itmDf = pd.DataFrame([rev for rev in itm_list if rev])
itmDf['site'] = 'ITM.'
nmeDf = pd.DataFrame([rev for rev in nme_df_list if rev])
nmeDf['site'] = 'NME.'
nrpDf = pd.DataFrame([rev for rev in nrp_list if rev])
nrpDf['site'] = 'NRP.'
owlDf = pd.DataFrame([rev for rev in owl_list if rev])
owlDf['site'] = 'OWL.'
pitcDf = pd.DataFrame([rev for rev in pitc_list if rev])
pitcDf['site'] = 'PIT.'
utrDf = pd.DataFrame([rev for rev in utr_list if rev])
utrDf['site'] = 'UTR.'
slantDf = pd.DataFrame([rev for rev in slant_list if rev])
slantDf['site'] = 'SLA.'
sputDf = pd.DataFrame([rev for rev in sput_list if rev])
sputDf['site'] = 'SPU.'
tmtDf = pd.DataFrame([rev for rev in tmt_list if rev])
tmtDf['site'] = 'TMT.'
syffDf = pd.DataFrame([rev for rev in syff_list if rev])
syffDf['site'] = 'SYF.'


reviewDf = pd.concat((bpmDf, avDf), 0)
reviewDf = pd.concat((reviewDf, apDf),0)
reviewDf = pd.concat((reviewDf, clashDf),0)
reviewDf = pd.concat((reviewDf, cmgDf),0)
reviewDf = pd.concat((reviewDf, cosDf),0)
reviewDf = pd.concat((reviewDf, diyDf),0)
reviewDf = pd.concat((reviewDf, exclaimDf),0)
reviewDf = pd.concat((reviewDf, hhdxDf),0)
reviewDf = pd.concat((reviewDf, itmDf),0)
reviewDf = pd.concat((reviewDf, nmeDf),0)
reviewDf = pd.concat((reviewDf, nrpDf),0)
reviewDf = pd.concat((reviewDf, owlDf),0)
reviewDf = pd.concat((reviewDf, pitcDf),0)
reviewDf = pd.concat((reviewDf, utrDf),0)

reviewDf = pd.concat((reviewDf, slantDf),0)
reviewDf = pd.concat((reviewDf, sputDf),0)
reviewDf = pd.concat((reviewDf, tmtDf),0)
reviewDf = pd.concat((reviewDf, syffDf),0)

reviewDf.columns = "artist", 'album', 'review', 'link', 'site'
reviewDf.to_pickle('phase1.pkl')
reviewDf = pd.read_pickle('phase1.pkl')


#USE ECHONEST API TO ADD WEIGHTED GENRE INFORMATION AND CLEAN ALBUM/ARTIST TITLE
#ALSO GET SPOTIFY ID


artistlst = []
albumlst = []

for k, each in enumerate(reviewDf['spotify_id']):
    print k
    if each:
        stuff = spotify.album(each)
        artistlst.append(stuff['artists'][0]['name'])
        albumlst.append(stuff['name'])
    else:
        artistlst.append(None)
        albumlst.append(None)
    
reviewDf['artist'] = artistlst
reviewDf['album'] = albumlst

mycoverlist = []
idlist = []
spotify = spotipy.Spotify()

counter = 0

for each in zip(reviewDf['artist'], reviewDf['album']):
    print counter
    counter += 1
    ARTIST, ALBUM = each
    try:
        results = spotify.search(q='album:'+ALBUM+' artist:'+ARTIST, type = 'album')
        items = results['albums']['items']
        if len(items) > 0:
            album = items[0]
            mycoverlist.append(album['images'][0]['url'])
            uri = album['uri']
            idlist.append(uri)
            albumname.append(album['name'])
        else:
            mycoverlist.append(None)
            idlist.append(None)
    except:
        mycoverlist.append(None)
        idlist.append(None)
        time.sleep(1)

reviewDf['albumcover'] = mycoverlist
reviewDf['spotify_id'] = idlist


#UPDATE DATAFRAME WITH CLEAN SPOTIFY INFORMATION
noNullDf = reviewDf.ix[list(np.where(reviewDf.notnull().all(axis=1))[0])].groupby('spotify_id').agg(lambda x: list(x))
noNullDf['artist'] = noNullDf['artist'].apply(lambda x: x[0])
noNullDf['album'] = noNullDf['album'].apply(lambda x: x[0])
noNullDf['review'] = noNullDf['review'].apply(lambda x: ' '.join(x).strip())
noNullDf['albumcover'] = noNullDf['albumcover'].apply(lambda x: x[0])

config.ECHO_NEST_API_KEY="XXXXXXXXXXXXX"
spotify = spotipy.Spotify()
genre_list = []

for i,each in enumerate(noNullDf['artist']):
    print i
    if i%9 == 0:
        time.sleep(10)

    try:
        k = artist.search(name = each)[0]
        temp = []
        for each in k.get_terms(sort='frequency'):
            temp.append((each['name'], each['weight']))
        genre_list.append(temp)
    except IndexError:
        print 'fail'
        genre_list.append(None)
        time.sleep(1)

noNullDf['genre'] = genre_list

noNullDf.to_pickle('phase2.pkl')

#REMOVE UNUSUAL CHARACTERS AND PUNCTUATION
noNullDf['review'] = noNullDf['review'].apply(lambda x: ''.join([ch for ch in x if ord(ch)<128]))
noNullDf['review'] = noNullDf['review'].apply(lambda x: re.sub(r'[^\w\s]', ' ', x))

#LEMMATIZE MY WORDS AND REMOVE ALL WORDS THAT AREN'T NOUNS OR ADJECTIVES
adjSeries = noNullDf['review']
lmtzr = WordNetLemmatizer()
adjSeries = adjSeries.apply(lambda x: [lmtzr.lemmatize(word) for word in x.split()])
adjSeries = adjSeries.apply(lambda x: [word[0] for word in pos_tag(x) if word[1] in ['JJ', 'NN']])
adjSeries = adjSeries.apply(lambda x: [word for word in x if len(word)>1])

#COMPILE SET OF ALL WORDS IN MY DATAFRAME
giant_wordlist = []
for each in adjSeries:
    giant_wordlist.extend(each)
giant_wordlist = set(giant_wordlist)

UD_synonyms = pickle.load(open('UD_synonyms'))

from crawlers.urbandictionary import *
#MAP MY WORDS TO A DICTIONARY THAT CONSISTS OF MY WORDS AND THEIR URBAN DICTIONARY SYNONYMS
for num, each in enumerate(list(giant_wordlist)):
    if each not in UD_synonyms.keys():
        UD_synonyms[each] = lookup_ud(each)
    if num%100==0:
        print num

#DEF A FLATTEN FUNCTION TO STANDARDIZE MY LISTS TO A SINGLE LIST OF WORDS
def flat(l):
    def _flat(l, r):
        if l == None:
            return r
        if type(l) not in [list, tuple]:
            r.append(l.lower())
        else:
            for i in l:
                r = r + flat(i)
        return r
    return _flat(l, [])


#MAP MY WORDLIST TO THE UD SYNONYMS
noNullDf['words2'] = adjSeries.apply(lambda x: [UD_synonyms[word] for word in x if UD_synonyms[word]!= "NOT FOUND"])
noNullDf['words2'] = noNullDf['words2'].apply(lambda x: flat(x))

for each in range(len(noNullDf)):
    noNullDf['words2'][each] = [word for word in noNullDf['words2'][each] if word not in [noNullDf['artist'][each], noNullDf['artist'][each].split()]]     

#LEMMATIZE MY WORDLIST
lmtzr = WordNetLemmatizer()
noNullDf['words2'] = noNullDf['words2'].apply(lambda x: [lmtzr.lemmatize(word) for word in x])
tfidf_vectorizer = TfidfVectorizer(min_df=0.05, stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['words2'].apply(lambda x: ' '.join(x)))
terms = tfidf_vectorizer.get_feature_names()


#ZIP MY TERMS WITH THEIR TFIDF WEIGHTS, INVERT SO WORDS MOST HIGHLY CORRELATED ARE 0 AND DISTANT ARE 1
terms_zip = []

for each in range(len(noNullDf)):
    terms_zip.append(zip(terms, tfidf_matrix.todense().tolist()[each]))

termsDf = pd.DataFrame(tfidf_matrix.todense().tolist())
termsDf = termsDf.div(termsDf.max()*1.)
termsDf = termsDf.apply(lambda x: 1-x)
termsDf.columns = terms
term_matrix = noNullDf[['artist', 'album', 'genre', 'albumcover']]
term_matrix = term_matrix.reset_index()
term_matrix = pd.concat((term_matrix, termsDf),1)

#RENAME MY COLUMNS TO PREVENT THEM FROM CLASHING WITH MY TERMS LIST
temp = list(term_matrix.columns)
temp[1] = 'artist_column'
temp[2] = 'album_column'
temp[3] = 'genre_column'
term_matrix.columns = temp
term_matrix['slug_column'] = term_matrix['artist_column'] + term_matrix['album_column']
term_matrix['slug_column'] = term_matrix['slug_column'].apply(lambda x: x.replace(' ', ''))


#OUTPUT TERM MATRIX TO PICKLE TO USE TO POPULATE MY MATRIX
term_matrix.to_pickle('term_matrix.pkl')



