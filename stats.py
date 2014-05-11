import os, sys
import math

f = open(sys.argv[1], 'r')
fstring = f.read()
lines = fstring.split('\n')
for l in lines:
    splits = l.split('|')
    name = splits[0]
    msd = splits[2].split(',')
    goog = splits[4].split(',')
    
    relevant_num = 0;

    msd_stats = {'pre':0, 'rec':0, 'dcg':0}
    goog_stats = {'pre':0, 'rec':0, 'dcg':0}

    for i in xrange(0,len(msd)):
        msd_stats['dcg'] += float(msd[i]) / math.log(i+2,2)
        goog_stats['dcg'] += float(goog[i]) / math.log(i+2,2)
        if (float(msd[i]) > 0):
            relevant_num += 1
            msd_stats['pre'] += 1
            msd_stats['rec'] += 1
        if (float(goog[i]) > 0):
            relevant_num += 1
            goog_stats['pre'] += 1
            goog_stats['rec'] += 1
    
    msd_stats['pre'] /= float(len(msd))
    msd_stats['rec'] /= float(relevant_num)
    goog_stats['pre'] /= float(len(msd))
    goog_stats['rec'] /= float(relevant_num)



    print 'Subject: '+name+':\n'
    print 'Google Precision: ' + str(goog_stats['pre']) + '\nMSD Precision: '+str(msd_stats['pre'])+'\n'
    print 'Google Recall: ' + str(goog_stats['rec']) + '\nMSD Recall: '+str(msd_stats['rec'])+'\n'
    print 'Google DCG: '+str(goog_stats['dcg'])+'\nMSD DCG: '+str(msd_stats['dcg'])+'\n\n'
    
