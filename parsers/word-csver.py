import ijson
import time
import codecs
from datetime import datetime
from time import strftime, localtime

#f = codecs.open("/media/storage/dpla-data/tmp.recs.2", 'r', encoding='utf-8')
#f = codecs.open("/media/storage/dpla-data/2016/10000.json", 'r', encoding='utf-8')
#f = open("/media/storage/dpla-data/2016/all.json")
f = open("/media/storage/dpla-data/nypl/nypl.json")

# Main output file

#This bit of data structure won't work in standard IO.
#To do this right, I'll need a database (or mongo)
#out = codecs.open('/media/storage/dpla-data/new/words/words.json', 'w', encoding='utf-8')

fields = ["identifier","collection","contributor","creator","date","description",
          "extent","format","identifier","isPartOf","language","publisher",
          "relation","rights","spatial","specType","stateLocatedIn","subject",
          "temporal","title","type","provider","subprov","thumbnail"]

colls = {    "ARTstor": "artstor",
             "Biodiversity Heritage Library": "biodiv",
             "David Rumsey": "rumsey",
             "Digital Commonwealth": "commonwealth",
             "Digital Library of Georgia": "georgia",
             "Harvard Library": "harvard",
             "HathiTrust": "hathi",
             "Internet Archive": "ia",
             "J. Paul Getty Trust": "getty",
             "Kentucky Digital Library": "kentucky",
             "Minnesota Digital Library": "minnesota",
             "Missouri Hub": "missouri",
             "Mountain West Digital Library": "mwdl",
             "National Archives and Records Administration": "nara",
             "North Carolina Digital Heritage Center": "nocar",
             "Smithsonian Institution": "smiths",
             "South Carolina Digital Library": "socar",
             "The New York Public Library": "nypl",
             "The Portal to Texas History": "texas",
             "United States Government Printing Office (GPO)": "gpo",
             "University of Illinois at Urbana-Champaign": "illinois",
             "University of Southern California. Libraries": "usc",
             "University of Virginia Library": "virginia",
             "nocoll": "nocoll"   
        }

#fieldfiles = {}
#collfiles = {}

#fieldfiles[s] = [codecs.open('/media/storage/dpla-data/new/words/fields/%s.txt' %s, 'w', encoding='utf-8') for s in fields]
#collfiles[s] = [codecs.open('/media/storage/dpla-data/new/words/colls/%s.txt' %s, 'w', encoding='utf-8') for s in colls.itervalues()]


# for field in fieldfiles: print field

#for s in fields:
#   fieldfiles[s] = codecs.open('/media/storage/dpla-data/words/fieldsnew/%s.new.txt' %s, 'w', encoding='utf-8')
#for s in colls.itervalues():
#   collfiles[s] = codecs.open('/media/storage/dpla-data/words/collsnew/%s.new.txt' %s, 'w', encoding='utf-8')

# for k,v in fieldfiles.iteritems():
#     print k
#     print v

# collfiles = [codecs.open('/media/storage/dpla-data/new/words/colls/%s.txt' %s, 'w', encoding='utf-8') for s in colls.itervalues()]

#textcsv = codecs.open('/media/storage/dpla-data/2016/words/text.csv', 'w', encoding='utf-8')
#weird = codecs.open('/media/storage/dpla-data/2016/words/weird.log', 'w', encoding='utf-8')
#debug = codecs.open('/media/storage/dpla-data/2016/words/debug.log', 'w', encoding='utf-8')

textcsv = codecs.open('/media/storage/dpla-data/nypl/words.text.csv', 'w', encoding='utf-8')
weird = codecs.open('/media/storage/dpla-data/nypl/words.weird.log', 'w', encoding='utf-8')
debug = codecs.open('/media/storage/dpla-data/nypl/words.debug.log', 'w', encoding='utf-8')
#write


now = ""
start =  time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
print "Start: " + start
counter = 0


for item in ijson.items(f, "item"):
    #print counter
    #print item['_source']['id']
    if "sourceResource" in item['_source'] and item['_source']['sourceResource'] is not None:
        counter = counter + 1
        if counter % 10000 == 0:
            now = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())
            print str(counter) + ": " + now
        if "provider" in item['_source']: 
            prov = item['_source']['provider']['name']
            #cname = colls[prov]
            #print cname
        else: 
            prov = "Null"
            #cname = "nocoll"
        if "dataProvider" in item['_source']:
            if isinstance(item['_source']['dataProvider'], basestring): subprov = item['_source']['dataProvider']
            else: subprov = ", ".join(item['_source']['dataProvider'])
        else: subprov = "Null"

        # collection, contributor, creator, date, description, extent, format, @id, identifier, 
        # isPartOf, language, publisher, relation, rights, spatial, specType, stateLocatedIn, 
        # subject, temporal, title, type

        for field in ["collection", "contributor", "creator", "date", "description", 
                      "extent", "format", "identifier", "isPartOf", "language", "publisher", 
                      "relation", "rights", "spatial", "specType", "stateLocatedIn", 
                      "subject", "temporal", "title", "type"]: 
            debug.write(unicode(item['_source']['id']) + "|" + unicode(field) + "\n")
            if field in item['_source']['sourceResource'] and item['_source']['sourceResource'][field] is not None:
                if isinstance(item['_source']['sourceResource'][field], list):
                    for entry in item['_source']['sourceResource'][field]:
                        debug.write(unicode(field) + "\n")
                        debug.write(unicode(entry) + "\n")
                        if isinstance(entry, dict):
                            if 'title' in entry.keys() and not isinstance(entry['title'], list):
                                textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(entry['title'].replace('\n','').replace('\r','')) + "\n")
                            elif 'title' in entry.keys() and isinstance(entry['title'], list):
                                textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(entry['title'][0].replace('\n','').replace('\r','')) + "\n")
                            elif 'displayDate' in entry.keys():
                                textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(entry['displayDate'].replace('\n','').replace('\r','')) + "\n")
                            elif 'name' in entry.keys():
                                textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(entry['name'].replace('\n','').replace('\r','')) + "\n")
                            elif 'city' in entry.keys():
                                textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(entry['city'].replace('\n','').replace('\r','')) + "\n")
                            elif 'state' in entry.keys():
                                textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(entry['state'].replace('\n','').replace('\r','')) + "\n")
                            elif 'country' in entry.keys():
                                textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(entry['country'].replace('\n','').replace('\r','')) + "\n")
                            elif '#text' in entry.keys():
                                textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(entry['#text'].replace('\n','').replace('\r','')) + "\n")
                            else:
                                textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(entry).replace('\n','').replace('\r','') + "\n")
                        elif isinstance(entry, list):
                            weird.write(item['_source']['id'] + "|" + field + "|" + unicode(entry) + "\n")
                        elif entry is not None:
                            textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(entry.replace('\n','').replace('\r','')) + "\n")
                elif isinstance(item['_source']['sourceResource'][field], dict):
                    debug.write(unicode(field) + "\n")
                    #print entry 
                    #print item['sourceResource'][field]
                    if 'title' in item['_source']['sourceResource'][field].keys():
                        textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(item['_source']['sourceResource'][field]['title'].replace('\n','').replace('\r','')) + "\n")
                    elif 'displayDate' in item['_source']['sourceResource'][field].keys():
                        if isinstance(item['_source']['sourceResource'][field]['displayDate'], dict):
                            weird.write(item['_source']['id'] + "|" + field + "|" + unicode(item['_source']['sourceResource'][field]['displayDate']) + "\n")
                        else: 
                            textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(item['_source']['sourceResource'][field]['displayDate'].replace('\n','').replace('\r','')) + "\n")
                    elif 'name' in item['_source']['sourceResource'][field].keys():
                        if isinstance(item['_source']['sourceResource'][field]['name'], list):
                            weird.write(item['_source']['id'] + "|" + field + "|" + unicode(item['_source']['sourceResource'][field]['name']) + "\n")
                        else:
                            textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(item['_source']['sourceResource'][field]['name'].replace('\n','').replace('\r','')) + "\n")
                    elif field == 'collection':
                        weird.write(item['_source']['id'] + "|" + field + "|" + unicode(item['_source']['sourceResource'][field]) + "\n")
                    elif not isinstance(item['_source']['sourceResource'][field], dict):
                        textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(item['_source']['sourceResource'][field].replace('\n','').replace('\r','')) + "\n")
                    else:  
                        debug.write(unicode(field) + "\n")
                        weird.write(unicode(item['_source']['sourceResource'][field]) + "\n")
                else:  
                    debug.write(unicode(field) + "\n")
                    textcsv.write(item['_source']['id'] + "|" + prov + "|" + subprov + "|" + field + "|" + unicode(item['_source']['sourceResource'][field].replace('\n','').replace('\r','')) + "\n")

    


end = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())

print "Start: " + start
print "End: " + end

# for f in fieldfiles:
#     close()
# for f in collfiles:
#     close()
