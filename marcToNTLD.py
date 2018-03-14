from csv import DictWriter
from pymarc import MARCReader
import re




def def500(string):
    #regexes to get dc values from undifferenciated notes fields.
    #problem-  some notes fields should be concated with other fields
    #problem a keyword field doesn't have anything to designated it as a keyword
    if re.search("[k,K]eyword.*", string['a']) != None:
        z = ( 'keywords', string['a'])
    if re.search('[F,f]aculty.*.',string['a']) != None:
        z = ('advisors', string['a'])
    elif re.search('[S,s]ponsor[s,:,\w]' ,string['a']) !=None:
        z = ('sponsor', string['a'] )
    elif re.search('(MQP[.][^\w]?)', string['a']) or re.search(('IQP[.][^\w]?'), string['a']) !=None :
        z = ('projectType', string['a'])
    return z



count = 0
#create the csv to write to.  Ignore errors to avoid unicode errors.  Examine it this is actually causing data loss
with open('C:\\Users\\amneslin\Documents\\eproj.csv','w',newline='', errors='ignore')as targetFile:
    fieldnames =['fileName', 'identifier', 'title', 'authors', 'advisors','sponsor', 'topic', 'abstract', 'projectType', 'keywords', 'year', 'publisher']
    writer = DictWriter(targetFile, fieldnames=fieldnames)
    writer.writeheader()
    #open the marc record.  This should be replaces with an argv in final
    with open('C:\\Users\\amneslin\Documents\\Digitzied eprojects.mrc', 'rb') as file:
        reader = MARCReader(file)
        for record in reader:
            # get fields that are explicitly defined by MARC tags
            creatorList=[]
            thing = {}
            title = (record.title())
            thing['title'] = title
            id= record['099']['a']
            thing['identifier'] = id
            filename = record['856']['u']
            thing['fileName'] = filename
            # use pass . If statement is pointless.  Remove at some point.  final except for testing purposes, remove
            try:
                publisher = record['260']['b']
                thing['publisher'] = publisher
            except:
                thing['publisher'] = 'no publisher'
            try:
                if  record['490']['a'] is not None:
                    topic = record['490']['a']
                    thing['topic'] = topic
            except: pass
            try:
                if record['440']['a'] is not None:
                    topic = record['440']['a']
                    thing['topic'] = topic
            except: pass
            try:
                if record['830']['a'] is not None:
                    topic = record['830']['a']
                    thing['topic'] = topic
            except:pass
            try:
                x= thing['topic']
            except:
                thing['topic'] = 'does it ever hit the end?'

            try:
                year = record['260']['c']
                thing['year'] = year
            except:
                year = record['260']
                thing['year'] = year
            try:
                abstract = record['520']['a']
                thing['abstract'] = abstract
            except:
                thing['abstract'] = ' '
            for note in record.get_fields('500'):
                try:
                    #execute function for notes fields
                    x=note
                    y=def500(x)
                    if y[1] == ("\t"): continue
                    field = y[0]
                    entry = y[1]
                    thing[field] = entry

                except:
                    continue
            #get all the students in the 700 fields and add them to one list
            for creators in record.get_fields('700'):
                if creators['e'] == 'Student author':
                    creatorList.append(creators['a'])
                creatorString=",".join(creatorList)
            thing['authors']=creatorString
            count = count+1
            writer.writerow(thing)
print (count)
targetFile.close()