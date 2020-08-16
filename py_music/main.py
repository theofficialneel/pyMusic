from __future__ import unicode_literals
import youtube_dl

from path import getPath, changePath
# from query import queryMusic
from spotify import metadataGen
from metascript import removeTags

# path = "./songs/"
path = getPath()

def asciiCheck(s):
	return all(ord(c)<128 for  c in s)

while 1:
	menu_input = int(input("\nMenu :\n[1] Query Music \n[2] Change Dest\n"))

	if menu_input == 1:
		yt_link = input("Enter link : ")

		with youtube_dl.YoutubeDL({}) as ydl:
			info_dict = ydl.extract_info(yt_link, download=False)
			yt_title = info_dict.get('title', None)

		while(not all(ord(c)<128 for  c in yt_title)):
			print("Error: \""+yt_title+"\" has non-ascii characters")
			yt_title = input("Enter new name : ")

		yt_title = removeTags(yt_title)

		ydl_opts = {
			'format': 'bestaudio/best',
			'outtmpl': path + yt_title + '.%(ext)s',
            'cachedir': False,
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '320',
			}],
		}
		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([yt_link])

		metadataGen(path, yt_title)

	elif menu_input == 2:
		print("Current path : " + path)
		temp_path = (input("Enter new path : ") or path)
			
		if path != temp_path:
			if not changePath(temp_path):
				print("Error: path doesn't exist")
				continue
			path = temp_path
			print("Success: Path changed")

	else:
		break

