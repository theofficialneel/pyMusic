from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import youtube_dl

path = "./songs/"

while 1:
	menu_input = input("\nMenu :\n1 : Query \n2 : Change Destination\n")

	if menu_input == 1:
		scrape_url="https://www.youtube.com"
		search_url="/results?search_query="
		search_hardcode = raw_input("Enter query : ")
		sb_url = scrape_url + search_url + search_hardcode

		sb_get = requests.get(sb_url)

		soupeddata = BeautifulSoup(sb_get.content, "html.parser")
		yt_links = soupeddata.find_all("a", class_ = "yt-uix-tile-link")
		i = 0
		yt3links = []
		for x in yt_links:
		 yt_href = x.get("href")
		 yt_title = x.get("title")
		 if "watch?" not in yt_href:
			continue
		 i = i + 1
		 if i > 3:
			break
		 yt_final = scrape_url + yt_href
		 yt3links.append(yt_final)
		 print str(i)+" : "+yt_title

		chosenLinkIndex = input("Pick (1-3) : ")

		ydl_opts = {
			'format': 'bestaudio/best',
			'outtmpl': path+'%(title)s.%(ext)s',
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '320',
			}],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([yt3links[chosenLinkIndex-1]])

	elif menu_input == 2:
		print "Current path : "+path
		path = (raw_input("Enter new path : ") or "./songs/")

	else:
		break

