Elster table from Jürg Müller website.

ElsterTable.inc
ErrorList.inc

Text is in German

eslter.py being a utility that translate the descritpion from german to one of the implemented language in google translate, takes a while so be patient, sometimes the utiity fails, looks like some timing problems while waiting fro google translation.

needs the python library google translate, argparse

  pip3 install googletrans==3.1.0a0

arguments

  -h help
  
  -a x languages available

  -l es (translate in spanish)

  -f file to translate either ElsterTable.json (default) or ErrorList.json
