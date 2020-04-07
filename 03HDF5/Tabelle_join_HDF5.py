# -*- coding: cp1252 -*-
#!/usr/bin/python
#-------------------------------------------------------------------------------
# Name:        Zum anjoinen von Attributen an bestehende HDF5-Tabellen
# Purpose:
#
# Author:      mape
#
# Created:     26/09/2016
# Copyright:   (c) mape 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import h5py
import pandas
import numpy as np
from numpy.lib.recfunctions import join_by
from pathlib import Path
path = Path.home() / 'python32' / 'python_dir.txt'
f = open(path, mode='r')
for i in f: path = i
path = Path.joinpath(Path(r'C:'+path),'Datenhaltung','Tabelle_an_HDF5.txt')
f = path.read_text()
f = f.split('\n')

#--Input--#
Datenbank = "V:"+f[0]
Group = f[1]
Tabelle = f[2]
Tabelle_join = f[3]


##################
#--Datenzugriff--#
##################
file5 = h5py.File(Datenbank,'r+') ##HDF5-File
group5 = file5[Group]

dset = group5[Tabelle]
dset_join = group5[Tabelle_join]

text = dset.attrs.values() ##Lese die Attribute dieser Tabelle
dset = np.array(dset) ##Umwandeln in ein Numpy-Dataset, damit die Bearbeitung schneller geht.
dset = pandas.DataFrame(dset)


################################
#--Beginne mit der Berechnung--#
################################
#--Join--#
"""
Vor dem joinen werden ersteinmal nur die Isochronen ausgewählt, die überhaupt gejoint werden sollen.
Ohne diesen Schritt braucht die Berechnung zu viel Rechenaufwand.
Der Join wird in Pandas ausgeführt.
Anschließend muss aus dem Pandas-Array wieder ein numpy-ndarry erstellt werden.
"""
Join1 = dset_join[np.in1d(dset_join["ZielHstBer"],dset["ZielHst"])]
Join2 = Join1[np.in1d(Join1["StartHstBer"],dset["StartHst"])]
Join2 = np.array(Join2) ##Erst an dieser Stelle, da erst nach dem Join der Array klein genug zum Umwadeln!
Join2 = pandas.DataFrame(Join2)

Join = pandas.merge(dset,Join2,'left',left_on = ["StartHst","ZielHst"],right_on = ["StartHstBer","ZielHstBer"]) ##Dies ist der entscheidende Join.


###########################
#--Generiere dtype array--#
###########################
#dtypes des neuen Pandas-arrays
dt = Join.dtypes
#Namen dieser dtypes. dtype = Datentyp
FN = Join.columns


######################################
#--Erzeuge die neue Ergebnistabelle--#
######################################
Spalten = []
for i in range(len(dt)):
    Spalten.append((FN[i],dt[i].name))
Spalten = np.dtype(Spalten) ##Wandle Spalten-Tuple in dtype um

Ergebnis = Join.as_matrix()
Ergebnis = list(map(tuple, Ergebnis)) ##Anpassen des Ergebnisarrays für den numpy dtype.

data = np.array(Ergebnis,Spalten)


###################################
#--Ergebnistabelle wird erstellt--#
###################################
del group5[Tabelle] ##Erst wird die alte Tabelle gelöscht
group5.create_dataset(Tabelle, data=data, dtype=Spalten) ##Dann wird die neue erstellt.

Ergebnis_T = group5[Tabelle]
Ergebnis_T.attrs.create("Parameter",text) ##Es werden die Attribute an die neue Tabelle angespielt.


#--Speichern--#
file5.flush()
file5.close()
