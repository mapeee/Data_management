# -*- coding: cp1252 -*-
##kleines Script, um Daten aus GIS in PGAdmin zu speichern
##Marcus Oktober 2013
##f�r Python 2.6.7

import arcpy
import time
import psycopg2
start_time = time.clock() ##Ziel: am Ende die Berechnungsdauer ausgeben

from pathlib import Path
path = Path.home() / 'python32' / 'python_dir.txt'
f = open(path, mode='r')
for i in f: path = i
path = Path.joinpath(Path(r'C:'+path),'Datenhaltung','GIS_in_pgadmin.txt')
f = path.read_text()
f = f.split('\n')


##Eingabe-Parameter
GIS = 'C:'+f[0]
TabName = "D_Gemeinden_2010"

##stellt Verbindung zu PGadmin her
pgadmin = psycopg2.connect(f[1])
pgcur = pgadmin.cursor()
try:
    pgcur.execute("DROP TABLE luftverkehr."+TabName)
    print TabName+" gel�scht!"
except:
    print "Keine Tabelle gel�scht."

##Fange Spaltennamen aus GIS ab
desc = arcpy.Describe(GIS)
fields = desc.fields
feld = ""
felder = ""
for field in fields:
    name = field.name
    typ = field.type
    if typ == "OID" or typ == "Geometry": ##Erstens nicht zu gebrauchen, zweitens ung�ltiges Format
        print "Spalte "+name+" wird nicht erstellt."
    else:
        feld = feld+name+" "+typ+", "
        felder = felder+name+", " ##damit Felder aus if-Klausel nicht in row reinrutschen!!

##Ersetzen der Feldnamen und Feldtypen falls mit PGadmin inkompatibel
feld = feld.replace("String","text") ##'string' durch 'text' ersetzen
feld = feld.replace("Double","double precision")
feld = feld.replace("SmallInteger","smallint")
feld = feld.replace("ANALYSE","ANALYSE_") ##wegen Analyse=SQL-Befehl in PGadmin!

##Erstelle die Tabelle in PGadmin
sql = "CREATE TABLE luftverkehr."+TabName+" ("+feld[:-2]+")"
pgadmin.commit()
pgcur.execute(sql)

##F�llen der Tabelle mit Werten
print "F�lle die neue PGadmin-Tabelle mit den GIS-Daten auf."
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
            VALUES = VALUES+"%s, " ##Baue die Klammer "Values(%s, %s, %s,...)
            a = row.getValue(name)
            l.append(a)##baue eine Liste mit den einzutragenden Werten!
    sql = "INSERT INTO luftverkehr."+TabName+" VALUES("+VALUES[:-2]+")"
    pgcur.execute(sql,l)
    row = rows.next()

##Verbindungen speichern und schlie�en
pgadmin.commit()
pgcur.close()  ##pgadmin
pgadmin.close() ##pgadmin

##Ende##
Sekunden = int(time.clock() - start_time)
Minuten = int(Sekunden/60)
Stunden = int(Minuten/60)
print "--Scriptdurchlauf erfolgreich nach",Stunden,"Stunden,",Minuten-(Stunden*60),"Minuten und",Sekunden-(Stunden*60*60+(Minuten-(Stunden*60))*60),"Sekunden!"
