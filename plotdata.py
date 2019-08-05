#!/usr/bin/env python

import numpy as np
import matplotlit.pyplot as plt
import os

infile = sys.argv[1]
column_number = sys.argv[2]


file = open(infile,’r’)
data = file.readlines()
file.close()


ydata = [ ]
for i in range(len(data)):
    ydata.append(data[i].split()[column_number])


plt.plot(ydata)
plt.show()