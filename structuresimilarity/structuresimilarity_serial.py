import numpy as np
#from pymatgen import MPRester
from matminer.featurizers.site import CrystalNNFingerprint
from matminer.featurizers.structure import SiteStatsFingerprint
import pandas
import pymatgen
import os
from mpinterfaces.calibrate import CalibrateSlab
from mpinterfaces.interface import Interface
from mpinterfaces import transformations
from mpinterfaces import utils

################################################################
#This script compares and picks out similar structures based on#
#statistical data repesenting the structural environment 	   #	
################################################################

#################################
# Uthpala Herath, November 2018 #
#################################

#connection with the MP API
#mpr = MPRester("IBaXLHT3blugPo07")

#poscar directory
directory='poscars'

#threashhold of dissimilarity to filter materials and save them. >0.9 means not similar
dissimilarity=0.9

#importing data from excel file
data_read = pandas.read_excel('All.xlsx')
data=data_read.dropna()

# dropping duplicte values 
data.drop_duplicates(subset ="MP_id",keep ="first",inplace=True ) 

#create empty dataframe to append data to later
df = pandas.DataFrame(columns=['MP_id1','material1','spg1','MP_id2','material2','spg2','distance'])

# Initialize structure fingerprints
ssf = SiteStatsFingerprint(CrystalNNFingerprint.from_preset('ops', distance_cutoffs=None, x_diff_weight=0),stats=('mean', 'std_dev', 'minimum', 'maximum'))

#looping over the materials
for i in range(len(data)):
    for j in range(len(data)):
        
        mpid1=data.MP_id.iloc[i]
        mpid2=data.MP_id.iloc[j]
        print("\n",data.pretty_formula.iloc[i]+"("+mpid1+") ? "+data.pretty_formula.iloc[j]+"("+mpid2+")")
        
        #get structures from MP given mpi id (in case you don't have poscars stored)
#        material1_st = mpr.get_structure_by_material_id(mpid1)
#        material2_st = mpr.get_structure_by_material_id(mpid2)
        #removed this because of the API timeout. Instead read poscars locally
        
        #use poscars to generate structure
        material1_st = pymatgen.io.vasp.Poscar.from_file(directory+os.sep+mpid1+os.sep+'POSCAR').structure
        material2_st = pymatgen.io.vasp.Poscar.from_file(directory+os.sep+mpid2+os.sep+'POSCAR').structure
        
        
        if (material1_st!=material2_st): #get rid of double counting
            v_material1 = np.array(ssf.featurize(material1_st))
            v_material2 = np.array(ssf.featurize(material2_st))
            distance = np.linalg.norm(v_material1-v_material2)
            
            if distance <= dissimilarity:
                print("SIMILARITY DETECTED!\n"+data.pretty_formula.iloc[i]+"("+mpid1+") = "+data.pretty_formula.iloc[j]+"("+mpid2+") @ "+"distance=",distance)
                material1=data.pretty_formula.iloc[i]
                material2=data.pretty_formula.iloc[j]
                spg1=data.spg.iloc[i]
                spg2=data.spg.iloc[j]
                df = df.append({'MP_id1':mpid1,'material1':material1,'spg1':spg1,'MP_id2':mpid2,'material2':material2,'spg2':spg2,'distance':distance}, ignore_index=True)
#store the similar materials in a Excel spreadsheet                
df.to_excel("similar_structures_serial.xlsx",index=False)

