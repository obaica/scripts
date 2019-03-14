#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 16:01:11 2018

@author: petavazohi

This script is used to generate the required poscars and append information to the excel file. 
"""

from pymatgen import MPRester, Composition
import pandas as pd
import os

mpr = MPRester("2ZsokqBcEb1dSuAM")

input_filename = "All.txt"

if not os.path.exists(input_filename[:-4]+'.xlsx'):
    data = pd.read_csv(input_filename, delimiter=r"\s+")
    data['MP_id'] = ''
    data['pretty_formula'] = ''
    data['link'] = 'https://materialsproject.org/materials/'
    data['spg']  = ''
    data['mp_icsds'] = ''
    data['searched'] = False
else : 
    data = pd.read_excel(input_filename[:-4]+'.xlsx')

if not os.path.exists("poscars"):
    os.mkdir("poscars")
ndata = len(data)
for idata in range(ndata):
    if data.searched.iloc[idata] == False : 
        iformula = data.Formula.iloc[idata]
        iicsd    = data.icsd.iloc[idata]
        comp = Composition(iformula)
        elements = []
        for ielement in comp.as_dict() : 
            elements.append(ielement)
        q_results = mpr.query({"elements": elements},properties=["pretty_formula", "structure","material_id"])
        for iquery in q_results : 
            mp_id = iquery["material_id"]
            structure = iquery["structure"]
            MP_data = mpr.get_data(mp_id)
            if iicsd in MP_data[0]['icsd_ids'] :
                mp_icsds = ''
                for item in MP_data[0]['icsd_ids'] : 
                    mp_icsds += '-' + str(item)
                data.MP_id.iloc[idata] = mp_id
                data.link.iloc[idata] += mp_id
                data.spg.iloc[idata]  = MP_data[0]['spacegroup']['number']
                data.pretty_formula.iloc[idata] = MP_data[0]['pretty_formula']
                data.mp_icsds.iloc[idata] = mp_icsds
                data.searched.iloc[idata] = True
                
                dir_path = "poscars"+os.sep+mp_id
                if not os.path.exists(dir_path):
                    os.mkdir(dir_path)
                structure.to (fmt='cif',filename=dir_path+os.sep+MP_data[0]['pretty_formula']+'.cif')
                structure.to (fmt='POSCAR',filename=dir_path+os.sep+"POSCAR")
                print(idata,MP_data[0]['pretty_formula'])
                data.to_excel("All.xlsx")
    else :
        print(idata,'already searched')
data.to_excel("All.xlsx")

