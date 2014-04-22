import hashlib
import sys, os
from operator import itemgetter

# Returns the possible tags for a given partial query
def getlist(tagpart):
    fn = hashlib.md5(tagpart).hexdigest()
    if (not os.path.exists('./QuerySuggestion')):
        raise NameError('No \'QuerySuggestion\' directory');
    if (not os.path.exists(os.path.join('QuerySuggestion',fn))):
        return [('--',1)]

    # First item in tag_list will be input so far
    tag_list = open(os.path.join('QuerySuggestion',fn), 'r').read().split('|')

    tuples = [None] * (len(tag_list)-1)

     # associate each tag with its location in the file (will be lost momentarily as we sort lexicographically), starting from the second one.
    for i in xrange(1, len(tag_list)):
       
        tuples[i-1] = (tag_list[i].split('\n')[0],i) # may contain newlines
        
    return sorted(tuples, key=itemgetter(0)); # sort by tag name for merging


# returns the intersection of list1 and list2, each associated with the sum of its ranks in both lists.
def intersect_lists(list1, list2):
    if (len(list1) > len(list2)): # list1 is shorter list
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
            tuples.append((list1[i][0], float(list1[i][1])+float(list2[j][1])))

    return tuples


# given a partial query string, returns all possible queries
def get_suggestions(partial_query):
    tag_parts = partial_query.split(' ')
    tuples = getlist(tag_parts[0])

    # intersect lists for all words
    for i in xrange(1, len(tag_parts)-1):
        tuples = intersect_lists(tuples, getlist(tag_parts[i]))
    
    suggestions = [None] 

    # sort by location as found (ties occur if we have tag1 and tag2 such that
    # tag1 appears in loc1 in list1, loc2 in list2 and tag2 appears in loc2 in 
    # list1, loc1 in list2, so reciprocal score = loc1+loc2 for each), breaking
    # ties arbitrarily.
    tuples = sorted(tuples, key=itemgetter(1)) 
    for i in xrange(0, len(tuples)):
        if (len(tuples[i][0].split(' ')) >= len(tag_parts)):
            suggestions[i] = tuples[i][0]

    return suggestions

f1 = open('QuerySuggestion/'+hashlib.md5('ro').hexdigest(), 'w');
f1.write('ro|rock n roll|rocking|rohypnol|rolypolar bear|roll');
f1.close()

f2 = open('QuerySuggestion/'+hashlib.md5('rol').hexdigest(), 'w');

f2.write('rol|rock n roll|roll tide|roll|rolling in the deep');
f2.close()

query = ''
for i in xrange(1, len(sys.argv)):
    query += sys.argv[i]+' '

print get_suggestions(query)





