# -*- coding: cp1252 -*-
#!/usr/bin/python

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mape
#
# Created:     10/05/2017
# Copyright:   (c) mape 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------


#---Vorbereitung---#
import xlrd ##nur zum lesen von Excel-Daten
import xlwt

XLS = 'C:'
results = 'C:'

#Spalten aus xls auswählen
Dokument = xlrd.open_workbook(XLS)
Blatt = Dokument.sheet_by_index(0) ##greift auf das erste (0) Tabellenblatt zu
Zeilen = Blatt.nrows-1 ##-1 wegen Überschriften
print("Es gibt ",Zeilen,"Zeilen!")

#--Neues Excel-File schreiben--#
wb = xlwt.Workbook() ##Ausgabedatei
ws = wb.add_sheet('Ergebnisse') ##Ausgabetabellenblatt
ws.write(0,0,"Nr")
ws.write(0,1,"Name")
ws.write(0,2,"Fachrichtung")
ws.write(0,3,"Strasse")
ws.write(0,4,"PLZ")
ws.write(0,5,"Ort")


#--Berechnung--#
for i in range(Zeilen):
    i+=1

    ws.write(i,0,i)
    ws.write(i,1,Blatt.cell_value(rowx=i,colx=0).replace("\n"," "))
    ws.write(i,2,Blatt.cell_value(rowx=i,colx=3).replace("\n"," "))

    Zelle = Blatt.cell_value(rowx=i,colx=1)
    Zelle = Zelle.split("\n")
    l = 0
    for e in Zelle:
        try:
            PLZ = int(e[:5])
            if PLZ < 10000:
                hh
            ws.write(i,4,PLZ)

            Ort = e.split(" ")[1]
            try: Ort= Ort+" "+Zelle[l+1]
            except:pass
            ws.write(i,5,Ort)

            Strasse = Zelle[0]
            if l==2:
                Strasse = Strasse+" "+Zelle[1]
            ws.write(i,3,Strasse)
        except: pass

        l+=1



#--Ergebnisse speichern--#
wb.save(results)
del wb, Dokument