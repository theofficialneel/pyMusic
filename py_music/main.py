from __future__ import unicode_literals
import requests

from bs4 import BeautifulSoup
import youtube_dl

from path import getPath, checkPath, changePath
from album import addAlbumArt

# path = "./songs/"
path = getPath()

def asciiCheck(s):
	return all(ord(c)<128 for  c in s)

while 1:
	menu_input = input("\nMenu :\n[1] Query Music \n[2] Change Dest\n")

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
			print "Error: \""+yt3titles[chosenLinkIndex-1]+"\" has non-ascii characters"
			yt3titles[chosenLinkIndex-1] = raw_input("Enter new name : ")

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

		addAlbumArt(path, yt3titles[chosenLinkIndex-1])

	elif menu_input == 2:
		print "Current path : " + path
		temp_path = (raw_input("Enter new path : ") or path)
			
		if path != temp_path:
			if not checkPath(path):
				print "Error: path doesn't exist"
				continue
			changePath(temp_path)
			path = temp_path
			print "Success: Path changed"

	else:
		break

