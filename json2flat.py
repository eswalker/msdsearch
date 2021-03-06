import sys
import json
import codecs


sys.stdout = codecs.getwriter('utf-8')(sys.stdout) 

if len(sys.argv) > 1:
    f = sys.argv[1]
else:
	print "usage: python json2flat.py <file_path>"
	sys.exit()

with open(f, 'r') as content_file:
    content = content_file.read()
    data = json.loads(content)
    tags = unicode("")
    numtags = 0
    for x in range(0, len(data["tags"])):
    	if data["tags"][x][1] != "0":
        	tags = tags + unicode("|") + unicode(data["tags"][x][0]) + unicode(",") + unicode(data["tags"][x][1]) 
        	numtags += 1
    if len(tags) != 0:
    	print data["track_id"] + "|" + data["artist"] + "|" + data["title"] + '|' + unicode(numtags) + tags
    	#print tags
