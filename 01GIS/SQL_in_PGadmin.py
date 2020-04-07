# -*- coding: cp1252 -*-
##kleines Script, um Daten in PG-Admin Tabelle zu speichern
##Marcus Oktober 2013
##für Python 2.6.7

import psycopg2
import sqlite3
import time
start_time = time.clock() ##Ziel: am Ende die Berechnungsdauer ausgeben

from pathlib import Path
path = Path.home() / 'python32' / 'python_dir.txt'
f = open(path, mode='r')
for i in f: path = i
path = Path.joinpath(Path(r'C:'+path),'Datenhaltung','SQL_in_pgadmin.txt')
f = path.read_text()
f = f.split('\n')


##Eingabe-Parameter
b = ("HAM_P2030U_Raster","HAJ_P2030U_Raster","BRE_P2030U_Raster","LBC_P2030U_Raster")

for TabNAME in b:
    ##stellt Verbindung zu SQL-Datenbank und PGAdmin her
    Datenbank = "V:"+f[0]
    conn = sqlite3.connect(Datenbank)
    c = conn.cursor()
    pgadmin = psycopg2.connect(f[1])
    pgcur = pgadmin.cursor()

    ##Fange die Spaltennamen und Attribute aus Starttabelle ab
    sql = "Select sql from sqlite_master where Name = '"+TabNAME+"'" ##über 'Mastertabelle'
    c.execute(sql)
    a = c.fetchall()
    a = a[0][0]
    a = a.replace("string","text") ##'string' durch 'text' ersetzen
    a = a.replace("double","double precision")
    a = a.replace("REAL","double precision")
    a = a.replace("NUM","text") ##'string' durch 'text' ersetzen
    a = a.replace("INT,","integer,") ##'string' durch 'text' ersetzen
    a = a.replace("GZeit,","GZeit double precision,") ##Sonderfall für Feld GZeit
    Schnitt = a.lstrip("CREATE TABLE "+TabNAME+" ")

    ##Speicher neue Tabelle in PGAdmin
    try:
        pgcur.execute("DROP TABLE luftverkehr."+TabNAME)
        print TabNAME+" gelöscht!"
    except:
        print "Keine Tabelle gelöscht."
    sql = str("CREATE TABLE luftverkehr."+TabNAME+" "+Schnitt)
    print sql
    pgadmin.commit() ##kurz speichern, kann sonst Probleme geben!
    pgcur.execute(sql)

    ##Füllen der Tabelle mit Werten
    sql = "Select * from "+TabNAME
    c.execute(sql)
    row = c.fetchone()
    while row:
        VALUES = ""
        x = len(row)
        while x > 0:
            VALUES = VALUES+"%s, "
            x = x-1        
        sql = "INSERT INTO luftverkehr."+TabNAME+" VALUES("+VALUES[:-2]+")" ##[:-2] trennt die beiden letzten Felder ab!
        pgcur.execute(sql,row)
        row = c.fetchone()
        
    pgadmin.commit()

    ##Verbindungen speichern und schließen
    conn.commit() ##sqlite3

    pgcur.close()  ##pgadmin
    pgadmin.close() ##pgadmin

##Ende##
Sekunden = int(time.clock() - start_time)
Minuten = int(Sekunden/60)
Stunden = int(Minuten/60)
print "--Scriptdurchlauf erfolgreich nach",Stunden,"Stunden,",Minuten-(Stunden*60),"Minuten und",Sekunden-(Stunden*60*60+(Minuten-(Stunden*60))*60),"Sekunden!"
