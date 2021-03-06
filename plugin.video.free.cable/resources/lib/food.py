import xbmcplugin
import xbmc
import xbmcgui
import urllib
import urllib2
import sys
import os
import re

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import demjson
import resources.lib._common as common

pluginhandle = int (sys.argv[1])

BASE_URL = 'http://www.foodnetwork.com/food-network-full-episodes/videos/index.html'
BASE = 'http://www.foodnetwork.com'

def masterlist():
    return rootlist(db=True)

def rootlist(db=False):
    data = common.getURL(BASE_URL)
    tree=BeautifulSoup(data, convertEntities=BeautifulSoup.HTML_ENTITIES)
    items=tree.find(attrs={'class':'playlists'}).findAll('a')
    db_shows = []
    for item in items:
        name = item.string.split('-')[0].replace('Full Episodes','').strip()
        url = BASE+item['href'].replace('channel-video/json/','feeds/channel-video/').replace(',00.json','_RA,00.json')
        if db==True:
            db_shows.append((name, 'food', 'show', url))
        else:
            common.addShow(name, 'food', 'show', url)
    if db==True:
        return db_shows
    else:
        common.setView('tvshows')

def show(url=common.args.url):
    data = common.getURL(url)
    videos = demjson.decode(data.split(' = ')[1])[0]['videos']
    for video in videos:
        if 'Season' in common.args.name:
            season = int(common.args.name.split('Season')[1])
            showname = common.args.name.split('Season')[0]
        else:
            showname = common.args.name
            season = 0
        #episode = int(video['number'])
        name = video['label']
        duration = video['length']
        thumb = video['thumbnailURL']
        description = video['description']
        airDate = video['delvStartDt']
        playpath = video['videoURL'].replace('http://wms.scrippsnetworks.com','').replace('.wmv','')
        url = 'rtmp://flash.scrippsnetworks.com:1935/ondemand?ovpfv=1.1'
        url+= ' swfUrl=http://common.scrippsnetworks.com/common/snap/snap-3.0.3.swf playpath='+playpath
        displayname = name
        infoLabels={ "Title":name,
                     "Season":season,
                     #"Episode":episode,
                     "Plot":description,
                     "premiered":airDate,
                     "Duration":duration,
                     "TVShowTitle":showname
                     }
        common.addVideo(url,displayname,thumb,infoLabels=infoLabels)
    common.setView('episodes')