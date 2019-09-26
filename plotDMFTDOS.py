#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
from builtins import open
from builtins import str
import matplotlib.pyplot as plt

with open('G_loc.out', 'r') as f:
    lines = f.readlines()
    x = [float(line.split()[0]) for line in lines]

    y_dz2 = [float(line.split()[2]) for line in lines]  #eg
    y_x2y2 = [float(line.split()[8]) for line in lines]


    y_dxz = [float(line.split()[4]) for line in lines]
    y_dyz = [float(line.split()[6]) for line in lines]  #t2g
    y_dxy = [float(line.split()[10]) for line in lines]

y_eg =[-1*sum(x)/3.14 for x in zip(y_dz2, y_x2y2)]   
y_t2g =[-1*sum(x)/3.14 for x in zip(y_dxz, y_dyz,y_dxy)]    
    
plt.figure(1)
plt.plot(x,y_eg,'r',label='$d-e_g$') 
plt.plot(x,y_t2g,'b',label='$d-t_{2g}$') 
plt.title('DMFT PDOS')  
plt.xlabel('Energy (eV)')
plt.ylabel('DOS (states eV/cell)')
plt.axvline(x=0,color='gray',linestyle='--')
plt.legend()
plt.savefig('DMFT-PDOS.png')
plt.show()

f.close()