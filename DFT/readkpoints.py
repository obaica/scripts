#!/usr/bin/env python
import numpy as np
import re

#Getting the high symmetry point names from KPOINTS file
f = open('KPOINTS')
KPread = f.read()
f.close()

KPmatrix = re.findall('reciprocal[\s\S]*',KPread)
tick_labels = np.array(re.findall('!\s(.*)',KPmatrix[0]))
knames=[]
knames=[tick_labels[0]]

for i in range(len(tick_labels)-1):
  if tick_labels[i] !=tick_labels[i+1]:
    knames.append(tick_labels[i+1])

knames = ['$'+latx+"$" for latx in knames] 


#getting the number of grid points from the KPOINTS file
f2 = open('KPOINTS')
KPreadlines = f2.readlines()
f2.close()
numgridpoints = int(KPreadlines[1].split()[0])

kticks=[0]
gridpoint=0
for kt in range(len(knames)-1):
  gridpoint=gridpoint+numgridpoints
  kticks.append(gridpoint-1)
print("knames        : ", knames)
print("kticks        : ", kticks)   