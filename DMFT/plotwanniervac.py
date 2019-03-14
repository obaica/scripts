#!/usr/bin/env python

import matplotlib.pyplot as plt
import re

outcar = open('OUTCAR', "r").read()
match = re.findall(r"E-fermi\s*:\s*(-?\d+.\d+)", outcar)[-1]


with open('wannier90_band.dat', 'r') as f:
    lines = list(line for line in (l.strip() for l in f) if line)
    x = [float(linex.split()[0]) for linex in lines]
    y = [(float(linex.split()[1])-float(match)) for linex in lines]  
 
ticks=[0,0.32901,1.01403,1.67523]
tickNames=['G','X','M','G']   
    
plt.figure(1)
plt.plot(x,y) 
plt.title('Wannier bands')  
plt.xticks(ticks,tickNames)
for xc in ticks:
    plt.axvline(x=xc,color='grey')
plt.xlim(ticks[0],ticks[-1])    
plt.ylabel('E-$E_F$')
plt.savefig('wannierbands.png')
plt.show()

f.close()

