import hashlib
import random
from operator import itemgetter
import sys
import os

# makes random inverted index files, for testing purposes, with name tagname and expected number of trackIDs 0.5*docnum
def makefile(tagname, docnum):
    f = open(hashlib.md5(tagname).hexdigest(), 'w')
    f.write(tagname)
    for i in xrange(0,docnum):
        if(random.random() > 0.5):
            f.write('|'+str(i)+','+str(random.random()))
    f.close()
             


# Return list of tracks and term weights sorted by trackID.
def getlist(tagnm):
    hashtag = hashlib.md5(tagnm).hexdigest()
    if (not os.path.exists(os.path.join('PostingsList', hashtag))):
         return [(0,0)]
    listfile = open(os.path.join('PostingsList', hashtag), 'r')
    plist = listfile.read().split('|')
    numtracks = len(plist)
    if (numtracks >=150):
        numtracks = 150;
    tuples = [None]*(numtracks-1)
    for i in xrange(1, numtracks):
        temp = plist[i].split(',')
        tuples[i-1] = (temp[0], float(temp[1]) + 1-i/1000000.0)
    return sorted(tuples)


# Return sorted list of tuples in format (trackID, weight1+weight2). Can use several calls to intersect several lists.
def intersectlists(list1, list2):
# arguments are lists of tuples, sorted by first member, 
# in format (trackID, weight).
    if (len(list1) > len(list2)): # force list1 to refer to shorter list
        temp = list1
        list1 = list2
        list2 = temp

    j = 0
    tuples = []
    for i in xrange(0, len(list1)): #iterate through shorter list adding values found in intersection of lists to return list.
        while (list2[j][0] < list1[i][0]):
            if (j+1 < len(list2)):
                j = j+1
            else:
                break
        if (list2[j][0] == list1[i][0]):
            #tuples.append((list1[i][0], list1[i][1], list2[j][1])
            tuples.append((list1[i][0], float(list1[i][1])+float(list2[j][1])))
    return tuples


# put tracks in descending order of total term weight
def sortedtracks(intersection):
    return sorted(intersection, key=itemgetter(1), reverse=True)

# takes list of tuples (trackID, weight) as args and outputs list of names of tracks in weight order as strings.
def tracknames(tuples):
    tracks = []
    tuples = sortedtracks(tuples)
    if (tuples[0][0] == 0):
        return ['no results found']

    for i in xrange(0, len(tuples)):
        if (not os.path.exists('Track/'+tuples[i][0])):
            tracks.append('not found '+tuples[i][0])
            continue
        else:
            tempfile = open('Track/'+tuples[i][0], 'r')
            temp = tempfile.read().split('|')
            tracks.append(temp[3] + ' ' +temp[2] +' ' + str(tuples[i][1]))
    return tracks


# make 3 new files and test functionality of above code.
def testing():
    makefile('incomprehensible screaming', 20)
    makefile('death metal', 20)
    makefile('classical', 20)
    list1 = getlist('incomprehensible screaming')
    list2 = getlist('death metal')
    list3 = getlist('classical')
    print list1
    print list2
    print list3
    
    intersection =  intersectlists(list1, list2)
    print intersection
    intersection2 = intersectlists(list3, intersection)
    print intersection2
    
    print sortedtracks(intersection2)


"""mainlist = getlist(sys.argv[1])
for i in xrange(2, len(sys.argv)):
   mainlist = intersectlists(mainlist, getlist(sys.argv[i]))

print sortedtracks(mainlist)
"""

