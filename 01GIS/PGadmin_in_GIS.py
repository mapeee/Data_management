# -*- coding: cp1252 -*-
##kleines Script, um Daten aus PGadmin in GIS zu speichern
##Marcus November 2013
##für Python 2.6.7

import arcpy
import time
import psycopg2
start_time = time.clock() ##Ziel: am Ende die Berechnungsdauer ausgeben

from pathlib import Path
path = Path.home() / 'python32' / 'python_dir.txt'
f = open(path, mode='r')
for i in f: path = i
path = Path.joinpath(Path(r'C:'+path),'Datenhaltung','GIS_in_SQL.txt')
f = path.read_text()
f = f.split('\n')

##Eingabe-Parameter
Methode = 1

GIS = "C:"+f[0]
TabName = f[1]

User = f[2]
Password = f[4]
dbname = f[5]
Schema = f[6]
Tabelle = f[7]
host= f[8]

if Methode == 1:
    ##stellt Verbindung zu PGadmin her und greift die SpaltenNamen und Typen ab
    pgadmin = psycopg2.connect("dbname='"+dbname+"' user='"+User+"'"+host+"' password='"+Password+"'")
    pgcur = pgadmin.cursor()

    sql = "Select * from information_schema.columns where table_schema='"+Schema+"' and table_name='"+Tabelle+"'"
    pgcur.execute(sql)
    a = pgcur.fetchall()

    ##Neue Tabelle in GIS erstellen
    if arcpy.Exists(GIS+"/"+TabName):
        arcpy.Delete_management(GIS+"/"+TabName)
        print "Folgende Tabelle wurde gelöscht: "+TabName+"!"
    arcpy.CreateTable_management(GIS,TabName)
    print "Folgende Tabelle wurde angelegt: "+TabName+"!"

    ##Spalten hinzufügen
    GIS = GIS+"/"+TabName ##Definiere den Pfad auf die neue Tabelle!
    for i in a:
        name = i[3]
        typ = i[7]
        if typ == "USER-DEFINED":
            print "Spalte "+name+" wird nicht erstellt."
        else:
            typ = typ.replace("double precision","Double")
            typ = typ.replace("bigint","integer")
            typ = typ.replace("character varying","string")
            typ = typ.replace("numeric","integer")
            arcpy.AddField_management(GIS,name,typ)
            print "Spalte "+name+" hinzugefügt."

    ##Zeilen aus PGadmin abfangen
    sql = "select * from "+Schema+"."+Tabelle
    pgcur.execute(sql)
    row = pgcur.fetchone()

    ##Werte in GIS überführen
    inrows = arcpy.InsertCursor(GIS)
    t_row = inrows.newRow()

    while row:
        row = reversed(row)
        row = tuple(row)
        z = 0 ##Zähler um die richtige Zeile bei setValue zu erwischen.
        for i in a:
            name = i[3]
            typ = i[7]
            if typ == "USER-DEFINED":
                z = z+1
                pass
            elif typ == "numeric" or typ == "bigint": ##muss wieder integers erstellen
                try: ##Falls Null-Value
                    t_row.setValue(name, int(row[z])) ##Par1 = Spaltenname, Par2 = Feldwert
                except:
                    t_row.setValue(name, row[z])
                z = z+1 ##muss eingerückt stehen, da row bereits bereinigt wurde!
            else:
                t_row.setValue(name, row[z]) ##Par1 = Spaltenname, Par2 = Feldwert
                z = z+1 ##muss eingerückt stehen, da row bereits bereinigt wurde!
        inrows.insertRow(t_row)
        row = pgcur.fetchone()

    del row, t_row, inrows
##Verbindungen speichern und schließen
pgadmin.commit()
pgcur.close()  ##pgadmin
pgadmin.close() ##pgadmin

##Ende##
Sekunden = int(time.clock() - start_time)
Minuten = int(Sekunden/60)
Stunden = int(Minuten/60)
print "--Scriptdurchlauf erfolgreich nach",Stunden,"Stunden,",Minuten-(Stunden*60),"Minuten und",Sekunden-(Stunden*60*60+(Minuten-(Stunden*60))*60),"Sekunden!"
