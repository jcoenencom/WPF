#!/usr/bin/python

from googletrans import Translator, constants
from pprint import pprint

import re
import json

f=open("ElsterTable.inc")

vars={}
ElsterTable={}
ErrorList={}
translator = Translator()

data=f.readlines()

for l in data:
    if (l[0:2] == '//'):
        pass
    elif ('=' in l):
        x=(l.split(' '))
        x.pop()
        var = re.sub('[\[\]]','',x.pop())
        vars[var]=[]
#        print(re.sub('[\[\]]','',var))
    elif ('{' in l):
        if('}' in l):
            x=(re.findall(r'\{(.*?)\}', l)[0].split(','))
            #print(x[1],'\t',x[0])
            vars[var].append(x)
#            nom[x[1]]=x[0]
#            type[x[1]]=x[2]
z=0
for key in vars:
    print(key)
    if (key == 'ErrorList'):
        print()
        for i in vars[key]:
            index=hex(int(i[0],16))
            text = i[1].replace('"','')
            translation = translator.translate(text,src="de",dest="fr")
            ErrorList[index]={}
            nom=translation.text
            ErrorList[index]=nom
            print(nom,flush=True) 
        with open('ErrorList.json','w') as f:
            json.dump(ErrorList,f)
            f.close()
        print('ErrorList file written')
    elif (key == 'ElsterTable'):
        print()
        for i in vars[key]:
            index=hex(int(i[1],16))
            ElsterTable[index]={}
            text = i[0].replace('"','')
            translation = translator.translate(text,src="de",dest="fr")
            nom=translation.text
            ElsterTable[index]['nom']=nom
            ElsterTable[index]['type']=i[2].strip()
            print(nom,flush=True)
        with open('ElsterTable.json','w') as f:
            json.dump(ElsterTable,f)
            f.close()
        print('ElsterTable file written')
print()
print(ErrorList)

print(ElsterTable)





