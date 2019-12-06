import os
import json
import urllib
from urllib2 import urlopen, Request, quote
from bs4 import BeautifulSoup

from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error

def makeAlbumFile(song_name):
    album_query = song_name + " album art"
    count = 3
    album_art_div = None
    while count:
        url = ("https://www.google.com/search?q=" + quote(album_query.encode('utf-8')) + "&source=lnms&tbm=isch")
        header = {
            'User-Agent':
            '''Mozilla/5.0 (Windows NT 6.1; WOW64)
            AppleWebKit/537.36 (KHTML,like Gecko)
            Chrome/43.0.2357.134 Safari/537.36'''
        }
        soup = BeautifulSoup(urlopen(Request(url, headers=header)), "html.parser")
        album_art_div = soup.find("div", {"class": "rg_meta"})
        if album_art_div:
            album_art = json.loads(album_art_div.text)["ou"]
            return album_art
        else:
            count = count - 1
        return None

def addAlbumArt(path, filename):
    url = makeAlbumFile(filename)
    if url:
        audio = MP3(path + filename + '.mp3', ID3=ID3)
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
                data=urlopen(url).read()
            )
        )
        audio.save()
