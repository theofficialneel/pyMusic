import re
import os

tags = [
    "official",
    "music",
    "lyric",
    "audio",
    "video",
    "kbps"
]

def removeTags(name):
    result = name
    search_results = re.findall('\(.*?\)',result)
    search_results += re.findall('\[.*?\]',result)
    for item in search_results:
        for tag in tags:
            if tag in item.lower():
                result = result.replace(item, "")
                break
    
    result = re.sub("feat\.", "ft", result, flags=re.I)
    result = re.sub("ft\.", "ft", result, flags=re.I)
    result = re.sub("\s+\.mp3", ".mp3", result).strip()
    result = re.sub("\s+", " ", result).strip()

    return result

def forceRemoveTags(name):
    result = re.sub(r'[^A-Za-z0-9 ]+', '', name)
    result = re.sub("ft", "", result, flags=re.I)
    result = re.sub("\s+", " ", result).strip()
    return result

def renameFiles(path):
    for dir, subdirs, files in os.walk(path):
        for f in sorted(files):
            f_new = removeTags(f)
            print(f + " >> " + f_new)
            os.rename(os.path.join(path, f), os.path.join(path, f_new))

# renameFiles("/home/neel/Pictures/testOffline/")