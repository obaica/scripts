#!/usr/bin/env python2
import sys, subprocess, os
import numpy as np
import shutil
from shutil import copyfile
import VASP
import Struct
from INPUT import *


#vasp executable
vasp_exec = "vasp_std"

#mpirun
if os.path.exists("para_com.dat"):
    fipa=open('para_com.dat','r')
    para_com=str(fipa.readline())[:-1]
    fipa.close()
else:
    para_com=""


print('\n#######################')
print('# DMFTwDFT initialization #')
print('##########################\n')

############initialization############################################

#generating wannier90.win
TB=Struct.TBstructure('POSCAR',p['atomnames'],p['orbs'])
TB.Compute_cor_idx(p['cor_at'],p['cor_orb'])
print(TB.TB_orbs)
DFT=VASP.VASP_class()
DFT.NBANDS=pV['NBANDS']
DFT.Create_win(TB,p['atomnames'],p['orbs'],p['L_rot'],DFT.NBANDS,DFT.EFERMI+p['ewin'][0],DFT.EFERMI+p['ewin'][1])

#initial DFT run
print('Running initial DFT...')
cmd = para_com+" "+vasp_exec
out, err = subprocess.Popen(cmd, shell=True).communicate()
print('Initial DFT calculation complete.\n')

#running wannier90.x to generate .chk
print('Running wannier90...')
cmd = "wannier90.x wannier90"
out, err = subprocess.Popen(cmd, shell=True).communicate()
print('wannier90 calculation complete.\n')

#generate sig.inp 
cmd = "sigzero.py"
out, err = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
print('Generated sig.inp.\n')

#creating directory for DMFT
if os.path.exists("DMFT"):
	shutil.rmtree("DMFT")
	os.makedirs("DMFT")
else:	
	os.makedirs("DMFT")

#copy INPUT.py to DMFT directory
copyfile("INPUT.py","./DMFT/INPUT.py")

#copying files into DMFT directory
cmd = "cd ./DMFT && Copy_input.py ../"
out, err = subprocess.Popen(cmd, shell=True).communicate()
print('DMFT initialization complete.\n')

