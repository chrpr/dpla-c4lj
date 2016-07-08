import ijson
import time
import codecs
from datetime import datetime
from time import strftime, localtime

#f = open("/media/storage/dpla-data/2016/all.json")
#out = codecs.open('/media/storage/dpla-data/2016/dpla.csv', 'w', encoding='utf-8')
#melt = codecs.open('/media/storage/dpla-data/2016/dpla.melt.csv', 'w', encoding='utf-8')
#log = codecs.open('/media/storage/dpla-data/2016/dpla.log.csv', 'w', encoding='utf-8')

f = open("/media/storage/dpla-data/nypl/nypl.json")
out = codecs.open('/media/storage/dpla-data/nypl/nypl.csv', 'w', encoding='utf-8')
melt = codecs.open('/media/storage/dpla-data/nypl/nypl.melt.csv', 'w', encoding='utf-8')
log = codecs.open('/media/storage/dpla-data/nypl/nypl.log.csv', 'w', encoding='utf-8')

now = ""
start =  time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
print "Start: " + start
counter = 0

melt.write("identifier|provider|subprov|url|field|binary|count\n")

header = "identifier|collection|contributor|creator|date|description|extent|format|identifier|"
header += "isPartOf|language|publisher|relation|rights|spatial|specType|stateLocatedIn|"
header += "subject|temporal|title|type|provider|subprov|url|thumbnail"
out.write(header + "\n")
for item in ijson.items(f, "item"):
    if "sourceResource" in item['_source'] and item['_source']['sourceResource'] is not None:
        counter = counter + 1
        if counter % 10000 == 0:
            now = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
            print str(counter) + ": " + now
        ident = item['_source']['id']
        #log.write(ident + "\n")
        if "provider" in item['_source']: prov = item['_source']['provider']['name']
        else: prov = "Null"
        if "dataProvider" in item['_source']:
            if isinstance(item['_source']['dataProvider'], basestring): subprov = item['_source']['dataProvider']
            else: subprov = ", ".join(item['_source']['dataProvider'])
        else: subprov = "Null"
        if "isShownAt" in item['_source']: shown = item['_source']['isShownAt']
        else: shown = "Null"
        string = ident
        # collection, contributor, creator, date, description, extent, format, @id, identifier, 
        # isPartOf, language, publisher, relation, rights, spatial, specType, stateLocatedIn, 
        # subject, temporal, title, type

        for field in ["collection", "contributor", "creator", "date", "description", 
                      "extent", "format", "identifier", "isPartOf", "language", "publisher", 
                      "relation", "rights", "spatial", "specType", "stateLocatedIn", 
                      "subject", "temporal", "title", "type"]: 

            if field in item['_source']['sourceResource'] and item['_source']['sourceResource'][field] is not None:
                melt.write(ident + "|" + prov + "|" + subprov + "|" + shown + "|" + field + "|1") 
                if isinstance(item['_source']['sourceResource'][field], list):
                    string += "|" + str(len(item['_source']['sourceResource'][field]))
                    melt.write("|" + str(len(item['_source']['sourceResource'][field])) + "\n")
                else:  
                    string += "|" + "1"
                    melt.write("|1\n")
            else: 
                string += "|" + "0"
                melt.write(ident + "|" + prov + "|" + subprov + "|" + shown + "|" + field + "|0|0\n")
    else:
        ident = item['_source']['id']
        log.write(ident + " has no sourceResource data.\n")    
    string += "|" + prov + "|" + subprov  + "|" + shown
    if 'object' in item:
        string += "|" + "1"
        melt.write(ident + "|" + prov + "|" + subprov + "|" + shown + "|thumb|1|1\n")
    else: 
        string += "|" + "0"
        melt.write(ident + "|" + prov + "|" + subprov + "|" + shown + "|thumb|0|0\n")

    out.write(string + "\n")
#objects = ijson.items(f, 'sourceResource')
#for o in objects:
#    print 'title'

end = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())

print "Start: " + start
print "End: " + end