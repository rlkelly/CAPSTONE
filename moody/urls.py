from django.conf.urls import patterns, url, include
from moody import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^add_artist/$', views.add_artist, name='add_album'),
    url(r'^art/(?P<artist_name_slug>[\w\-]+)/$', views.art, name='art'),
    

    #url(r'^album/(?P<album_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
 
    #url(r'^register/$', views.register, name='register'),
    #url(r'^login/$', views.user_login, name='login'),
    #url(r'^logout/$', views.user_logout, name='logout'),
    #url(r'^search/', views.search, name='search'),
 
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^goto/$', views.track_url, name='goto'),
    url(r'^like_artist/$', views.like_artist, name='like_artist'),
    url(r'^suggest_artist/$', views.suggest_artist, name='suggest_artist'),
    url(r'^album/(?P<album_name_slug>[\w\-]+)/$', views.album, name='album'),
    url(r'^word/(?P<word_slug>[\w\-]+)/$', views.word, name='word'),
    url(r'^genre/(?P<genre_slug>[\w\-]+)/$', views.genre, name='genre'),
    url(r'^search/$', views.search, name='search'),
    )