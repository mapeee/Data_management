# -*- coding: cp1252 -*-

##Script zum erstellen einer Liste aus einer Matrix##
##Januar 2014
##Marcus
print "Script zum Umwandeln einer Matrix in eine x-y-Liste."

import xlrd ##nur zum lesen von Daten
import xlwt ##nur zum schreiben von Daten
import csv
from pathlib import Path
path = Path.home() / 'python32' / 'python_dir.txt'
f = open(path, mode='r')
for i in f: path = i
path = Path.joinpath(Path(r'C:'+path),'Datenhaltung','Matrix_in_Liste.txt')
f = path.read_text()
f = f.split('\n')


##Parameter##
Pfad = "V:"+f[0]
Ergebnis= "V:"+f[1]
Zeilen = 0 ##x Zeilen bis zum relevanten Inhalt
Spalten = 2 ##y Spalten bis zum relevanten Inhalt

####Eingabe vorbereiten####
book = xlrd.open_workbook(Pfad)
print "Es gibt insgesamt", book.nsheets, "Tabellenblätter."
sh = book.sheet_by_index(0) ##greift auf das erste (0) Tabellenblatt zu
print "Das Tabellenblat",sh.name,"hat",sh.nrows,"Zeilen und",sh.ncols,"Spalten."
print "Inhalt der linken, oberen Ecke lautet:", sh.cell_value(rowx=0+Zeilen, colx=0+Spalten)

####Ausgabe vorbereiten####
wb = xlwt.Workbook() ##Ausgabedatei
ws = wb.add_sheet('A Test Sheet') ##Ausgabetabellenblatt

##Ausgabestyles (Beispiele)##
style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',num_format_str='#,##0.00')
style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
from datetime import datetime ##zur Ausgabe von Datem und Zeit in Excel
##ws.write(0, 0, 1234.56, style0)##Beispiel
##ws.write(1, 0, datetime.now(), style1)##Beispiel

##Bereichszähler##
xz = 0
for i in range(Zeilen,sh.nrows):
    leer = sh.cell_value(rowx=i, colx=0+Spalten)
    if leer == "": ##Durchsuche alle relevanten Zeilen bis zur ersten Leerzeile, falls  vorhanden!
        break
    else:
        xz=xz+1
print "Es gibt",xz,"relevante Zeilen in der Fahrtenmatrix."
xz = xz-1 ##Da ja die Namenszeile kein Wertepaar bildet!

xs = 0
for i in range(Spalten,sh.ncols):
    leer = sh.cell_value(rowx=0+Zeilen, colx=i)
    if leer == "":
        break
    else:
        xs=xs+1
print "Es gibt",xs,"relevante Spalten in der Fahrtenmatrix."
xs = xs-1 ##Da ja die Namensspalte kein Wertepaar bildet!

if xz!=xs:
    print "Achtung, Zeilen und Spalten sind nicht gleich!!"
    
##Eingabe-Schleife##
print("Beginne mit dem Füllen des Ausgabeblattes.")

f = 0 ##Zeilenzähler für jede Aktion
for i in range(Spalten,xs+Spalten): ##Da erst im relevanten Bereich begonnen wird und alles nach hinten zu verschieben ist.
    for j in range(Zeilen,xz+Zeilen):
        ws.write(f,0,sh.cell_value(rowx=Zeilen, colx=i+1)) ##Zeile,Spalte,Inhalt
        ws.write(f,1,sh.cell_value(rowx=j+1, colx=Spalten)) ##Zeile,Spalte,Inhalt
        ws.write(f,2,sh.cell_value(rowx=j+1, colx=i+1)) ##Zeiele,Spalte,Inhalt
        f = f+1

wb.save(Ergebnis)
del xlrd, xlwt

print "Fertig!!"
