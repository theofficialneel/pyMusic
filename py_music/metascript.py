import re
import os

tagwords = [
    "official music video",
    "official lyrics video",
    "official lyric video",
    "official music",
    "official audio",
    "official video",
    "music video",
    "lyric video",
    "lyrics video",
    "lyrics",
    "320  kbps",
    "256  kbps",
    "192  kbps",
    "\(audio\)",
    "\(lyric\)",
    "\(\)",
    "\[\]"
]

def removeTags(name):
    result = name
    for word in tagwords:
        result = re.sub(word, "", result, flags=re.I)

    result = re.sub("feat\.", "ft", result, flags=re.I)
    result = re.sub("ft\.", "ft", result, flags=re.I)
    result = re.sub("\s+\.mp3", ".mp3", result).strip()
    result = re.sub("\s+", " ", result).strip()

    return result

def renameFiles(path):
    for dir, subdirs, files in os.walk(path):
        for f in sorted(files):
            f_new = removeTags(f)
            print f + " >> " + f_new
            os.rename(os.path.join(path, f), os.path.join(path, f_new))

# renameFiles("/home/neel/Pictures/testOffline/")