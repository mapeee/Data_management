# -*- coding: cp1252 -*-
##kleines Script, um Daten von .db3-Datenbank in GIS zu Speichern.
##Marcus Oktober 2013
##für Python 2.6.7

import arcpy
import sqlite3
import time
start_time = time.clock() ##Ziel: am Ende die Berechnungsdauer ausgeben

from pathlib import Path
path = Path.home() / 'python32' / 'python_dir.txt'
f = open(path, mode='r')
for i in f: path = i
path = Path.joinpath(Path(r'C:'+path),'Datenhaltung','SQL_in_GIS.txt')
f = path.read_text()
f = f.split('\n')

##Eingabe-Parameter
TabNAME = "OV_Flaeche"
GIS = "C:"+f[0]

##stellt Verbindung zu SQL-Datenbank her
Datenbank = "V:"+f[1]
conn = sqlite3.connect(Datenbank)
c = conn.cursor()

##Fange die Spaltennamen und Attribute aus Starttabelle ab
sql = "PRAGMA table_info( "+TabNAME+" )"
c.execute(sql)
a = c.fetchall()

##Neue Tabelle in GIS erstellen
if arcpy.Exists(GIS+"/"+TabNAME):
    arcpy.Delete_management(GIS+"/"+TabNAME)
    print "Folgende Tabelle wurde gelöscht: "+TabNAME+"!"
arcpy.CreateTable_management(GIS,TabNAME)
print "Folgende Tabelle wurde angelegt: "+TabNAME+"!"

##Spalten hinzufügen
GIS = GIS+"/"+TabNAME ##Definiere den Pfad auf die neue Tabelle!
def addfield(Par1,Par2,Par3): ##Definiere die Funktion 'addfield' mit drei Parametern
    arcpy.AddField_management(Par1, Par2, Par3) ##Par1=Pfad, Par2=Name, Par3=Typ
for i in a:
    z = i[2] ##teilweise andere Bennung in SQL
    z = z.replace("NUM","text")
    z = z.replace("INT,","integer,") ##das Komma, damit aus INTEGER nicht intEGER wird!
    z = z.replace("REAL","double")
    addfield(GIS,i[1],z)
    print "Spalte "+str(i[1])+" hinzugefügt."

##Werte in GIS überführen
inrows = arcpy.InsertCursor(GIS) ##Setze Cursor zum Einfügen in die Ergebnistabelle
t_row = inrows.newRow() ##erstellt ein leeres Zeilenobjekt
sql = "SELECT * From "+TabNAME
c.execute(sql)
row = c.fetchone() ##rufe erste Zeile ab
def addvalue(Par1,Par2): ##definierte Funktion zum Feld hinzufügen
    t_row.setValue(Par1, Par2) ##Par1 = Spaltenname, Par2 = Feldwert
print "Feldwerte werden hinzugefügt!"

while row: ##für jede Zeile
    for i in a: ##Spalten aus SQL-PRAGMA
        f = i[1] ##Spaltenname
        z = row[i[0]] ##Holt den Wert aus row[xy] und und Spalte mit der Nummer i[0] aus a.
        addvalue(f,z)
    inrows.insertRow(t_row)
    row = c.fetchone()
    
del row, t_row, inrows
##Verbindungen speichern und schließen
conn.commit() ##sqlite3

##Ende##
Sekunden = int(time.clock() - start_time)
Minuten = int(Sekunden/60)
Stunden = int(Minuten/60)
print "--Scriptdurchlauf erfolgreich nach",Stunden,"Stunden,",Minuten-(Stunden*60),"Minuten und",Sekunden-(Stunden*60*60+(Minuten-(Stunden*60))*60),"Sekunden!"
