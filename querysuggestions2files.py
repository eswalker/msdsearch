import hashlib
import sys

path = "QuerySuggestion/"

for line in sys.stdin:
	key = line.split('|')[0].lower().strip(' \t\n\r')
	has = hashlib.md5(key).hexdigest()
	f = open(path + has,'w')
	f.write(line) # python will convert \n to os.linesep
	f.close()
