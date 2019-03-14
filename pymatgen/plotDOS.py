#!/usr/bin/env python

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import DosPlotter

v = Vasprun('vasprun.xml')
cdos = v.complete_dos
element_dos = cdos.get_element_dos()
plotter = DosPlotter()
plotter.add_dos_dict(element_dos)
plotter.show(xlim=[-2, 2], ylim=[-10, 10])
