import os
from ConfigParser import SafeConfigParser

curr_path = os.path.dirname(__file__)
par_path = os.path.abspath(os.path.join(curr_path, os.pardir))

def getPath():
	parser = SafeConfigParser()
	parser.read(os.path.join(par_path,'settings.ini'))
	path = parser.get('PATH', 'value')
	return path

def changePath(new_path):
	if not os.path.isdir(new_path):
		return False
		
	parser = SafeConfigParser()
	parser.read(os.path.join(par_path,'settings.ini'))
	parser.set('PATH', 'value', new_path)
	with open(os.path.join(par_path,'settings.ini'), 'wb') as configfile:
		parser.write(configfile)

	return True