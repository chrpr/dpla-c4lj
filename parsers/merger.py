# merger.py

import re
import codecs

#analyt = codecs.open("/media/Windows7_OS/dpla/new/dpla.analytics.weekly.csv", 'r', encoding='utf-8')
#meta = codecs.open("/media/Windows7_OS/dpla/new/dpla.csv", 'r', encoding='utf-8')
#metaplus = codecs.open("/media/Windows7_OS/dpla/new/dpla.merged2.csv", 'w', encoding='utf-8')

#analyt = codecs.open("/media/storage/dpla-data/words/colls.oct/analytics/dpla.analytics.weekly.csv", 'r', encoding='utf-8')
#meta = codecs.open("/media/storage/dpla-data/words/colls.oct/analytics/dpla.csv", 'r', encoding='utf-8')
#metaplus = codecs.open("/media/storage/dpla-data/words/colls.oct/analytics/dpla.merged.2015.csv", 'w', encoding='utf-8')

analyt = codecs.open("/media/storage/dpla-data/2016/dpla.hits.csv", 'r', encoding='utf-8')
meta = codecs.open("/media/storage/dpla-data/2016/dpla.csv", 'r', encoding='utf-8')
# Here, merged 1 is merging in the local data. 
# We may also want to merge in referrals _out_ based on x-ref to the collected other data.
# Then check those column counts...
metaplus = codecs.open("/media/storage/dpla-data/2016/dpla.merged.csv", 'w', encoding='utf-8')
merge_errors = codecs.open("/media/storage/dpla-data/2016/merge.errors.csv", 'w', encoding='utf-8')
analythash = {}
found = []

for line in analyt:
    parsed = line.split("|")
    match = re.search('(?<=^/item/)[^?./]*|(?<=^/item/).*$', parsed[0])
    #match = re.search('(?<=^/item/).*[?]', parsed[0])
    if match and len(match.group(0)) == 32: 
        #print match.group(0)
        analythash[match.group(0)] = parsed[1]
    #else: print parsed[0]
    #print parsed[0]
    #print line

#for k,v in analythash.items():
#    print ('Item %s has been accessed %s times' % (k,v.rstrip()))

for line in meta:
    parsed = line.split("|")
    iden = parsed[0]
    if iden == "identifier":
        metaplus.write(line.rstrip() + "|analytics\n")
    elif iden in analythash:
        metaplus.write(line.rstrip() + "|" + str(analythash[iden]).rstrip() + "\n")
        found.append(iden)
    else:
        metaplus.write(line.rstrip() + "|0\n")

for line in analyt:
    parsed = line.split("|")
    match = re.search('(?<=^/item/)[^?./]*|(?<=^/item/).*$', parsed[0])
    if match and len(match.group(0)) == 32: 
        if match not in found:
            merge_errors.write(match + "|Not in dpla data")
    else:
        merge_errors.write(match + "|Not valid dpla id")