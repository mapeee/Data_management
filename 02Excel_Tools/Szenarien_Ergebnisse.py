# -*- coding: cp1252 -*-
#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:        Finale Indikatoren der Radschnellwege
# Purpose:
#
# Author:      mape
#
# Created:     14/11/2016
# Copyright:   (c) mape 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import h5py
import numpy as np
import pandas

import xlrd
import xlwt
from pathlib import Path
path = Path.home() / 'python32' / 'python_dir.txt'
f = open(path, mode='r')
for i in f: path = i
path = Path.joinpath(Path(r'C:'+path),'Datenhaltung','Szenarien_Ergebnisse.txt')
f = path.read_text()
f = f.split('\n')


#--Parameter--#
Datenbank = "V:"+f[0]
Group = "E_Varianten"
XLSX = "V:"+f[1]
Raster_EW = "Raster_EW"


#--Neues Excel-File schreiben--#
wb = xlwt.Workbook() ##Ausgabedatei
ws = wb.add_sheet('Ergebnisse') ##Ausgabetabellenblatt

#--Datenzugriff--#
file5 = h5py.File(Datenbank,'r+') ##HDF5-File
group5 = file5[Group]


#--Varianten--#
ws.write(0,0,"Variante")
n = 1
for i in group5.keys():
    if "Vergleich" in i:
        var = i.split("ergleich_")[1]
        ws.write(n,0,var)
        n = n+1


#--Indikatoren_EW--#
dset_EW = group5["Raster_EW"]
dset_EW = np.array(dset_EW)
dset_EW = pandas.DataFrame(dset_EW)

#--Indikatoren--#
ws.write(0,1,"EW35")
ws.write(0,16,"Zellen")

ws.write(0,2,"APSUM10absEWabs")
ws.write(0,3,"APSUM10absEWrel")
ws.write(0,4,"APSUM10relEWrel")

ws.write(0,5,"APSUM20absEWabs")
ws.write(0,6,"APSUM20absEWrel")
ws.write(0,7,"APSUM20relEWrel")

ws.write(0,8,"APEXP050absEWabs")
ws.write(0,9,"APEXP050absEWrel")

ws.write(0,10,"GymCLOSEabsEWabs")
ws.write(0,11,"GymCLOSEabsEWrel")

ws.write(0,12,"BahnCLOSEabsEWabs")
ws.write(0,13,"BahnCLOSEabsEWrel")

ws.write(0,14,"ShopCLOSEabsEWabs")
ws.write(0,15,"ShopCLOSEabsEWrel")


#--Schleife ueber die Varianten--#
n = 1
for i in group5.keys():
    if "Vergleich" in i:
        print i
        dset = group5[i]
        dset = np.array(dset)
        dset = pandas.DataFrame(dset)

        #--Close--# ##In den Vergleichstabellen sind teilw. sehr niedrige Werte für Ziele, die im Nufallfall nicht erreicht wurden (999). Um hier keine Verzerrungen zu erreichen, werden die ersetzt!
        dset["GymCLOSEabs"][dset["GymCLOSEabs"]<-20] = -10 ##Wähle die Spalte "xy" über die Index dieser Spalte, wo der Wert unter -20 liegt und ersetze ihn dann!
        dset["BahnCLOSEabs"][dset["BahnCLOSEabs"]<-20] = -10
        dset["ShopCLOSEabs"][dset["ShopCLOSEabs"]<-20] = -10

        #--Merge--#
        dset = pandas.merge(dset,dset_EW,left_on="ID",right_on="ID")

        #--Berechne die Indikatoren--##
        #Sonstige
        ws.write(n,1,sum(dset["EW"]))
        ws.write(n,16,len(dset))
        #AP10
        a = dset[dset["APSUM10abs"]>0]
        ws.write(n,2,sum(a["EW"]))
        ws.write(n,3,int(sum(a.EW*a.APSUM10abs)/sum(a.EW)))
        ws.write(n,4,sum(a.EW*a.APSUM10rel)/sum(a.EW))
        #AP20
        a = dset[dset["APSUM20abs"]>0]
        ws.write(n,5,sum(a["EW"]))
        ws.write(n,6,int(sum(a.EW*a.APSUM20abs)/sum(a.EW)))
        ws.write(n,7,sum(a.EW*a.APSUM20rel)/sum(a.EW))
        #AP50Exp
        a = dset[dset["APEXP050abs"]>0]
        ws.write(n,8,sum(a["EW"]))
        ws.write(n,9,int(sum(a.EW*a.APEXP050abs)/sum(a.EW)))
        #GymCLOSE
        a = dset[dset["GymCLOSEabs"]<0]
        ws.write(n,10,sum(a["EW"]))
        try: ##Falls keine Verbesserung
            ws.write(n,11,sum(a.EW*a.GymCLOSEabs)/sum(a.EW))
        except:
            ws.write(n,11,0)
        #BahnCLOSE
        a = dset[dset["BahnCLOSEabs"]<0]
        ws.write(n,12,sum(a["EW"]))
        try: ##Falls keine Verbesserung
            ws.write(n,13,sum(a.EW*a.BahnCLOSEabs)/sum(a.EW))
        except:
            ws.write(n,13,0)
        #ShopCLOSE
        a = dset[dset["ShopCLOSEabs"]<0]
        ws.write(n,14,sum(a["EW"]))
        try: ##Falls keine Verbesserung
            ws.write(n,15,sum(a.EW*a.ShopCLOSEabs)/sum(a.EW))
        except:
            ws.write(n,15,0)


        n = n+1


#--Speichern--#
wb.save(XLSX)
print "fertig!!!"
