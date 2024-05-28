#!/usr/bin/python

from googletrans import Translator, constants
import argparse
from pprint import pprint

import re
import json

LANGUAGES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'he': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'}

parser=argparse.ArgumentParser()
parser.add_argument('-l',dest='language', type=str, help='translate to ... (default==en)')
parser.add_argument('-f',dest='file',type=str,help='file to translate default is ElserTable.inc')
parser.add_argument("-a",dest='aide', help='Available Languages')
args=parser.parse_args()


if (args.aide):
    print('Available languages\n')
    for i in LANGUAGES.keys():
        print(LANGUAGES[i],i)
    quit()

if (args.language):
    target = args.language
else:
    target='en'

if (args.file):
    f=args.file
else:
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
            translation = translator.translate(text,src="de",dest=target)
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
            translation = translator.translate(text,src="de",dest=target)
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
