# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 10:48:38 2018

@author: mape
"""

import csv
from pathlib import Path
path = Path.home() / 'python32' / 'python_dir.txt'
f = open(path, mode='r')
for i in f: path = i
path = Path.joinpath(Path(r'C:'+path),'Datenhaltung','csv_Bearbeitung.txt')
f = path.read_text()
f = f.split('\n')


ifile = open('C:'+f[0], 'rb')

ofile  = open('C:'+f[1], "wb")
writer = csv.writer(ofile, delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL)

reader = csv.reader(ifile)
i = 0
for row in reader:
    if i == 0:continue
    i+=1
    if i >30:break
    print(row[0])
    
        
ifile.close()
ofile.close()
