#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import bs4, sys, math, re, MySQLdb, types, urllib, urllib2, datetime, random, time, unicodedata, base64, socket
from urlparse import urljoin
from urllib2 import URLError
from datetime import datetime

'''
CREATE TABLE IF NOT EXISTS `youtube_gaming_channels_most_subscribed` (
  `channel` varchar(255) NOT NULL,
  `views` bigint(20) unsigned NOT NULL DEFAULT '0',
  `subscribers` bigint(20) unsigned NOT NULL DEFAULT '0',
  `videos` bigint(20) unsigned NOT NULL DEFAULT '0',
  `friends` bigint(20) unsigned NOT NULL DEFAULT '0',
  `date_joined` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`channel`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8;
'''

url='http://vidstatsx.com/youtube-top-100-most-subscribed-games-gaming-channels'
hostname = '54.88.34.236'
username = 'gamera'
password = 'gamera@1234'
dbname = 'gamera'

con = MySQLdb.connect(host=hostname, port=3306, 
    user=username, passwd=password, db=dbname)
cursor = con.cursor()

def openurl(urls):
  req = urllib2.Request(urls)
  ok=False
  try:
    res = urllib2.urlopen(req)
    info = res.info()
    html = res.read()
    ok=True
  except IOError, e:
    ok=False
    print 'IOError', e

  if not ok:
    sys.exit(0)

  return html

def getListOfUrls():
  urlList = []
  html = openurl(url)
  soup = bs4.BeautifulSoup(html)
  for script in soup.findAll('script'):
    script.extract()

  for tr in soup.find_all('tr')[:]:
    for link in tr.findAll('a', {'class': "user"}, href=True):
      urlList.append(link['href'])
  return urlList

def getChannelNameEnglish(endOfAddress):
  name = endOfAddress.partition('/')
  realName = name[2].partition('/')
  return str(realName[0])

def insertYoutubeChannel(name, views, subscribers, uploads, friends, dateJoined):
  global cursor

  print 'testing ', name   
  sql = "SELECT * FROM youtube_gaming_channels_most_subscribed WHERE channel = \'" + name + "\'"
  cursor.execute(sql)
  result = cursor.fetchone()

  # dateJoined = datetime.strptime(dateJoined, '%Y-%m-%d')
  
  if result:
    print 'exists ', name 
    sql = "UPDATE `youtube_gaming_channels_most_subscribed` SET `channel`=\"%s\",`views`=%s,`subscribers`=%s,`videos`=%s,`friends`=%s,`date_joined`=\"%s\" WHERE 1"  % \
            (name, views, subscribers, uploads, friends, dateJoined)
    updateinsert = "update"
  else:
    print 'inserting ',name
    sql = "INSERT INTO `youtube_gaming_channels_most_subscribed`(`channel`, `views`, `subscribers`, `videos`, `friends`, `date_joined`) VALUES (\"%s\",%s,%s,%s,%s,\"%s\")" % \
          (name, views, subscribers, uploads, friends, dateJoined)
    updateinsert = "insert"
  print sql
  try:
    cursor.execute(sql)
  except:
    print 'failed %s for %s' % (updateinsert, name)
    pass
  return True


urls = getListOfUrls()

for url in urls:
  name = getChannelNameEnglish(url)
  url = "http://vidstatsx.com" + url

  html = openurl(url)

  soup = bs4.BeautifulSoup(html)
  for script in soup.findAll('script'):
    script.extract()

  statsList = []
  for tr in soup.find_all('tr')[:]:
    stats = tr.find_all('td', {'class': "rank green"})
    for stat in stats:
      statsList.append(stat.text)
  
  if len(statsList) == 13:
    statsList.insert(0,"0")  
    statsList.insert(6,"0")  
  if len(statsList) == 15:
    del(statsList[0])
    del(statsList[0])
    del(statsList[5])
    del(statsList[5])
    del(statsList[5])
    del(statsList[5])
    del(statsList[5])
    del(statsList[5])
    del(statsList[5])



  uploads = int(statsList[0].replace(',', ''))
  subscribers = int(statsList[3].replace(',', ''))
  views = int(statsList[5].replace(',', ''))
  friends = int(statsList[1].replace(',', ''))
  subscriptions = int(statsList[4].replace(',', ''))
  dateJoined = statsList[2]
  dateJoined = datetime.strptime(dateJoined, '%b %d, %Y')

  insertYoutubeChannel(name, views, subscribers, uploads, friends, dateJoined)
