# -*- coding: cp1252 -*-
#!/usr/bin/python
##kleines Script, um Daten aus GIS in SQL-Tabelle zu speichern
##Marcus Oktober 2013
##für Python 2.6.7

import arcpy
import time
import sys

try: ##greift vermutlich auf falsche Version (64-bit) zurück, darum neue Pfadsetzung.
    import sqlite3
except:
    sys.path = ['C:\\Python26\\Lib', 'C:\\Python26\\DLLs', 'C:\\Python26\\Lib\\lib-tk']
    import sqlite3

start_time = time.clock() ##Ziel: am Ende die Berechnungsdauer ausgeben

from pathlib import Path
path = Path.home() / 'python32' / 'python_dir.txt'
f = open(path, mode='r')
for i in f: path = i
path = Path.joinpath(Path(r'C:'+path),'Datenhaltung','GIS_in_SQL.txt')
f = path.read_text()
f = f.split('\n')

##Eingabe-Parameter
GIS = "C:"+f[0]
Datenbank = "V:"+f[1]
TabName = "testerr"

##stellt Verbindung zu SQL-Datenbank her
conn = sqlite3.connect(Datenbank)
c = conn.cursor()
c.execute("Drop Table if Exists %s" %TabName)

##Fange Spaltennamen aus GIS ab
desc = arcpy.Describe(GIS)
fields = desc.fields
sql = ""
felder = ""
for field in fields:
    bb
    name = field.name
    typ = field.type
    if typ == "OID" or typ == "Geometry": ##Erstens nicht zu gebrauchen, zweitens ungültiges Format
        print "Spalte "+name+" nicht erstellt."
    else:
        sql = sql+name+" "+typ+", "
        felder = felder+name+", " ##damit 'Shape' nicht in row reinrutscht!!
        
print "Lege SQL-Tabelle an."
sql = "CREATE TABLE "+TabName+" ("+sql[:-2]+")" ##[:-2] trennt die beiden letzten Zeichen ab!
c.execute(sql)

##Füllen der Tabelle mit Werten
print "Fülle die neue SQL-Tabelle mit den GIS-Daten auf."
rows = arcpy.SearchCursor(GIS,"","",felder[:-2]) ##Setzt den Abfrage-Cursor auf die Tabelle!
row = rows.next()
while row:
    VALUES = ""
    l = []  ##erzeuge eine neue, leere Liste!
    for field in fields:
        name = field.name
        typ = field.type
        if typ == "OID" or typ == "Geometry":
            pass
        else:
            VALUES = VALUES+"?,"
            a = row.getValue(name)
            l.append(a)
    sql = "INSERT INTO "+TabName+" VALUES("+VALUES[:-1]+")"
    c.execute(sql,l)
    row = rows.next()

##Verbindungen speichern und schließen
conn.commit() ##sqlite3

##Ende##
Sekunden = int(time.clock() - start_time)
Minuten = int(Sekunden/60)
Stunden = int(Minuten/60)
print "--Scriptdurchlauf erfolgreich nach",Stunden,"Stunden,",Minuten-(Stunden*60),"Minuten und",Sekunden-(Stunden*60*60+(Minuten-(Stunden*60))*60),"Sekunden!"
