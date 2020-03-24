import requests
from bs4 import BeautifulSoup

def asciiCheck(s):
	return all(ord(c)<128 for  c in s)

def queryMusic(query_string):
    scrape_url="https://www.youtube.com"
    search_url="/results?search_query="
    sb_url = scrape_url + search_url + query_string
    sb_get = requests.get(sb_url)

    soupeddata = BeautifulSoup(sb_get.content, "html.parser")
    yt_links = soupeddata.find_all("a", {'class' : "yt-uix-tile-link"})
    yt_times = soupeddata.find_all("span", {'class' : "video-time"})
    yt_meta_data = soupeddata.find_all("ul", {'class' : "yt-lockup-meta-info"})
    yt_channel = soupeddata.find_all("div", {'class' : "yt-lockup-byline"})
    i = 0
    j = 0
    yt = []

    for link in yt_links:
        yt_link_href = link.get("href")
        yt_link_title = link.get("title")
        yt_duration = str(yt_times[j].text)
        yt_channel_a = yt_channel[i].find_all("a")
        yt_meta = yt_meta_data[i].find_all("li")
        i = i + 1
        if "watch?" not in yt_link_href or "&list" in yt_link_href:
            continue
        if len(yt_meta) >= 2:
            yt_time_stamp = str(yt_meta[0].text)
            yt_views = str(yt_meta[1].text)
        else:
            continue
        yt_channel_name = yt_channel_a[0].text
        j = j + 1
        if j > 3:
            break

        yt_info = {
            'count': str(j),
            'title': yt_link_title,
            'link': scrape_url + yt_link_href,
            'duration': yt_duration,
            'views': yt_views,
            'time': yt_time_stamp,
            'channel': yt_channel_name
        }
        yt.append(yt_info)

    return yt