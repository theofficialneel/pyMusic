from __future__ import unicode_literals

from bs4 import BeautifulSoup
import os
import requests
import json
from urllib2 import urlopen, Request, quote
import urllib
from ConfigParser import SafeConfigParser

import youtube_dl
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

# path = "./songs/"
parser = SafeConfigParser()
parser.read('../settings.ini')
path = parser.get('SETTINGS', 'value')

def asciiCheck(s):
	return all(ord(c)<128 for  c in s)

def albumArtGen(name):
	album = name + " Album Art"
	url = ("https://www.google.com/search?q=" + quote(album.encode('utf-8')) + "&source=lnms&tbm=isch")
	header = {
		'User-Agent':
			'''Mozilla/5.0 (Windows NT 6.1; WOW64)
			AppleWebKit/537.36 (KHTML,like Gecko)
			Chrome/43.0.2357.134 Safari/537.36'''
	}

	soup = BeautifulSoup(urlopen(Request(url, headers=header)), "html.parser")

	albumart_div = soup.find("div", {"class": "rg_meta"})
	albumart = json.loads(albumart_div.text)["ou"]

	urllib.urlretrieve(albumart, "temp-album-art.jpg")



while 1:
	menu_input = input("\nMenu :\n[1] Query \n[2] Change Dest\n")

	if menu_input == 1:
		scrape_url="https://www.youtube.com"
		search_url="/results?search_query="
		search_hardcode = raw_input("Enter query : ")
		sb_url = scrape_url + search_url + search_hardcode

		sb_get = requests.get(sb_url)

		soupeddata = BeautifulSoup(sb_get.content, "html.parser")
		yt_links = soupeddata.find_all("a", class_ = "yt-uix-tile-link")
		yt_times = soupeddata.find_all("span", {'class' : "video-time"})
		yt_meta_data = soupeddata.find_all("ul", {'class' : "yt-lockup-meta-info"})
		i = 0
		j = 0
		yt3links = []
		yt3titles = []
		for x in yt_links:
			yt_href = x.get("href")
			yt_title = x.get("title")
			yt_duration = str(yt_times[j].text)
			yt_meta = yt_meta_data[i].find_all("li")
			yt_views = "-"
			yt_time_stamp = "-"
			if len(yt_meta) >= 2:
				yt_time_stamp = str(yt_meta[0].text)
				yt_views = str(yt_meta[1].text) 
			i = i + 1
			if "watch?" not in yt_href:
				continue
			j = j + 1
			if j > 3:
				break
			yt_final = scrape_url + yt_href
			yt3titles.append(yt_title)
			yt3links.append(yt_final)
			print "["+str(j)+"] "+yt_title+" ["+yt_duration+"]"
			print "<"+yt_views+"> - <"+yt_time_stamp+">\n"

		chosenLinkIndex = input("Pick [1-3] ")

		while(not asciiCheck(yt3titles[chosenLinkIndex-1])):
			print "The Title \""+yt3titles[chosenLinkIndex-1]+"\" seems to have a non ascii character"
			yt3titles[chosenLinkIndex-1] = raw_input("Please enter a new name : ")

		ydl_opts = {
			'format': 'bestaudio/best',
			'outtmpl': path+yt3titles[chosenLinkIndex-1]+'.%(ext)s',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '320',
			}],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([yt3links[chosenLinkIndex-1]])

		albumArtGen(yt3titles[chosenLinkIndex-1])

		audio = MP3(path+yt3titles[chosenLinkIndex-1]+'.mp3', ID3=ID3)
		try:
		    audio.add_tags()
		except error:
		    pass

		audio.tags.add(
		    APIC(
		        encoding=3, # 3 is for utf-8
		        mime='image/png', # image/jpeg or image/png
		        type=3, # 3 is for the cover image
		        desc=u'Cover',
		        data=open('temp-album-art.jpg').read()
		    )
		)
		audio.save()

		os.remove("temp-album-art.jpg")

	elif menu_input == 2:
		
		print "Current path : " + path
		temp_path = (raw_input("Enter new path : ") or path)
		
		if not os.path.isdir(temp_path):
			print "Sorry the path you typed doesnt exist."
			continue

		parser.set('SETTINGS', 'value', temp_path)
		with open('../settings.ini', 'wb') as configfile:
			parser.write(configfile)
			
		if path != temp_path:
			print "Path changed"

		path = temp_path

	else:
		break

