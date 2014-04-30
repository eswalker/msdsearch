import sys

path = "Track/"

for line in sys.stdin:
	key = line.split('|')[0]
	f = open(path + key,'w')
	f.write(line)
	f.close()