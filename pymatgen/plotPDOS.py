#!/usr/bin/env python
from pymatgen.io import vasp
import numpy as np
import matplotlib.pyplot as plt

vasprun = vasp.Vasprun('vasprun.xml')   
#dos = vasprun.complete_dos
#
#site = vasprun.structures[0][4]
#
#partial_t2g = dos.get_site_t2g_eg_resolved_dos(site)['t2g']
#partial_t2g = np.zeros_like(partial_t2g.get_densities())
#partial_eg = dos.get_site_t2g_eg_resolved_dos(site)['e_g']
#partial_eg = np.zeros_like(partial_eg.get_densities())
#
#for i in range(4,8): # for all the Ni atoms
#  site = vasprun.structures[0][i] 
#  partial_t2g_i = dos.get_site_t2g_eg_resolved_dos(site)['t2g'] 
#  partial_t2g += partial_t2g_i.get_densities() 
#  partial_eg_i = dos.get_site_t2g_eg_resolved_dos(site)['e_g'] 
#  partial_eg += partial_eg_i.get_densities()
#  
#plt.plot((partial_t2g_i.energies-dos.efermi),partial_t2g,'b')
#plt.plot((partial_eg_i.energies-dos.efermi),partial_eg,'r')
#
#plt.axvline(x=0.0, color='k', linestyle='--')
#
#plt.xlabel('Energy (eV)')
#plt.ylabel('DOS')
#plt.title('Density of States')



from pymatgen.electronic_structure.plotter import DosPlotter

data1 = vasprun.complete_dos.get_site_t2g_eg_resolved_dos(vasprun.structures[0][4])
data2 = vasprun.complete_dos.get_site_t2g_eg_resolved_dos(vasprun.structures[0][5])
data3 = vasprun.complete_dos.get_site_t2g_eg_resolved_dos(vasprun.structures[0][6])
data4 = vasprun.complete_dos.get_site_t2g_eg_resolved_dos(vasprun.structures[0][7])


plot = DosPlotter()
plot.add_dos("Ni(d-t$_2g$)",data1['t2g']+data2['t2g']+data3['t2g']+data4['t2g'])
plot.add_dos("Ni(d-e$_g$)",data1['e_g']+data2['e_g']+data3['e_g']+data4['e_g'])


plot.show()
plot.save_plot("DOS.png",img_format="png")