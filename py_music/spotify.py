import os
from ConfigParser import SafeConfigParser
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

curr_path = os.path.dirname(__file__)
par_path = os.path.abspath(os.path.join(curr_path, os.pardir))

def enable_connection():
    parser = SafeConfigParser()
    parser.read(os.path.join(par_path,'settings.ini'))
    cid = parser.get('SPOTIFY', 'id')
    secret = parser.get('SPOTIFY', 'secret')
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def spotify_search(query_name):
    sp = enable_connection()
    results = sp.search(q=query_name, limit=3, type='track')

    if len(results["tracks"]["items"]) == 3:
        i = 0
        spot_obj = {
            "album": "",
            "artists": [],
            "release_date": "",
            "genres": [],
            "image_url": "",
        }

        while i < 3:
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
                print(json.dumps(spot_obj, indent=4, sort_keys=False))
                break