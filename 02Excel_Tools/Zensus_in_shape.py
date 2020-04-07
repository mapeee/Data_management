# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 13:49:12 2019

@author: mape
"""

import csv
import arcpy
from pathlib import Path
path = Path.home() / 'python32' / 'python_dir.txt'
f = open(path, mode='r')
for i in f: path = i
path = Path.joinpath(Path(r'C:'+path),'Datenhaltung','Zensus_in_Shape.txt')
f = path.read_text()
f = f.split('\n')

csvfile = open('C:'+f[0], 'rb')
reader = csv.reader(csvfile,delimiter=';')

fc = 'C:'+f[1]
cursor = arcpy.da.InsertCursor(fc, ["SHAPE@XY","Gitter_100_ID","EW"])


i = 0
for row in reader:
    a = row
    if i == 0:
        i+=1
        continue
    if int(a[1])>4500000:continue
    if int(a[1])<4196000:continue
    if int(a[2])<3245000:continue
    if int(a[3])<0:
        a[3] = 0
    i+=1
    
    xy = ((int(a[1]), int(a[2])),a[0],int(a[3]))

    cursor.insertRow(xy)
        
csvfile.close()
