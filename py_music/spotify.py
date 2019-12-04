import os
import re
import json
import urllib
from urllib2 import urlopen
from ConfigParser import SafeConfigParser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB, TDRC, TYER, TCON, error

from album import addAlbumArt

curr_path = os.path.dirname(__file__)
par_path = os.path.abspath(os.path.join(curr_path, os.pardir))

def enableConnection():
    parser = SafeConfigParser()
    parser.read(os.path.join(par_path,'settings.ini'))
    cid = parser.get('SPOTIFY', 'id')
    secret = parser.get('SPOTIFY', 'secret')
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def spotifySearch(query_name):
    sp = enableConnection()
    results = sp.search(q=query_name, limit=3, type='track')
    i = 0
    spot_obj = {
        "album": "",
        "artists": [],
        "release_date": "",
        "genres": [],
        "image_url": "",
    }

    while i < len(results["tracks"]["items"]):
        obj = results["tracks"]["items"][i]
        if obj["album"]["album_type"] == "compilation":
            i = i + 1
        else:
			gen_list = []
			spot_obj["album"] = obj["album"]["name"]
			spot_obj["release_date"] = obj["album"]["release_date"]
			spot_obj["image_url"] = obj["album"]["images"][0]["url"]
			for artist in obj["artists"]:
				spot_obj["artists"].append(artist["name"])
				a_id = artist["id"]
				a_res = sp.artist(a_id)
				gen_list.extend(a_res["genres"])
			for genre in gen_list:
				if genre not in spot_obj["genres"]:
					spot_obj["genres"].append(genre)
			break

    # print(json.dumps(spot_obj, indent=4, sort_keys=False))
    return spot_obj

def modifyQueryName(query):
	x = re.sub("[\(\[].*?[\)\]]", "", query)
	i = x.lower().find("ft.")
	j = x.lower().find("feat.")
	i = len(x) if i==-1 else i
	j = len(x) if j==-1 else j
	x = x[:i][:j]
	return x

def metadataGen(path, filename):
	x = modifyQueryName(filename)
	s_obj = spotifySearch(x)
	print(json.dumps(s_obj, indent=4, sort_keys=False))

	if s_obj["image_url"] == "":
		addAlbumArt(path, filename)
	else:
		audio = MP3(path + filename + '.mp3', ID3=ID3)
		try:
			audio.add_tags()
		except error:
			pass
		audio.tags.add(TIT2(text=filename))
		audio.tags.add(TPE1(text=s_obj["artists"]))
		audio.tags.add(TALB(text=s_obj["album"]))
		audio.tags.add(TDRC(text=(s_obj["release_date"][:4])))
		audio.tags.add(TYER(text=(s_obj["release_date"][:4])))
		audio.tags.add(TCON(text=s_obj["genres"]))
		audio.tags.add(
			APIC(
				encoding=3, # 3 is for utf-8
				mime='image/png', # image/jpeg or image/png
				type=3, # 3 is for the cover image
				desc=u'Cover',
				data=urlopen(s_obj["image_url"]).read()
			)
		)
		audio.save()
