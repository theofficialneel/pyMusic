import os
from ConfigParser import SafeConfigParser

def getPath():
    parser = SafeConfigParser()
    parser.read('../settings.ini')
    path = parser.get('SETTINGS', 'value')

    return path

def checkPath(path):
    if not os.path.isdir(temp_path):
		return False
    return True

def changePath(path):
    parser.set('SETTINGS', 'value', path)
    with open('../settings.ini', 'wb') as configfile:
        parser.write(configfile)