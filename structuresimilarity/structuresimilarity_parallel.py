import numpy as np
#from pymatgen import MPRester
from matminer.featurizers.site import CrystalNNFingerprint
from matminer.featurizers.structure import SiteStatsFingerprint
import pandas
from multiprocessing import Pool
import os
from pymatgen.io import vasp
#
#from mpinterfaces.calibrate import CalibrateSlab
#from mpinterfaces.interface import Interface
#from mpinterfaces import transformations
#from mpinterfaces import utils

################################################################
#This script compares and picks out similar structures based on#
#statistical data repesenting the structural environment 	   #	
################################################################

#################################
# Uthpala Herath, November 2018 #
#################################

#processors
procs=4

#poscar directory
directory='poscars'

#threashhold of dissimilarity to filter materials and save them. >0.9 means not similar
dissimilarity=0.9

#importing data from excel file
data_read = pandas.read_excel('All_test.xlsx')
data=data_read.dropna()

# dropping duplicte values 
data.drop_duplicates(subset ="MP_id",keep ="first",inplace=True ) 

#create empty dataframe to append data to later
df = pandas.DataFrame(columns=['MP_id1','material1','spg1','MP_id2','material2','spg2','distance'])

# Initialize structure fingerprints
ssf = SiteStatsFingerprint(CrystalNNFingerprint.from_preset('ops', distance_cutoffs=None, x_diff_weight=0),stats=('mean', 'std_dev', 'minimum', 'maximum'))


def match(args):
  mpid1 = args[0]
  mpid2 = args[1]
  material1 = args[2]
  material2 = args[3]
  spg1 = args[4]
  spg2 = args[5]
  
  mpid1_list = []
  mpid2_list = []
  material1_list = []
  material2_list = []
  spg1_list = []
  spg2_list = []
  distance_list=[]
  
   
  #print("\n",data.pretty_formula.iloc[i]+"("+mpid1+") ? "+data.pretty_formula.iloc[j]+"("+mpid2+")")
  print("\n",material1+"("+mpid1+") ? "+material2+"("+mpid2+")")

  #use poscars to generate structure
  material1_st = vasp.Poscar.from_file(directory+os.sep+mpid1+os.sep+'POSCAR').structure
  material2_st = vasp.Poscar.from_file(directory+os.sep+mpid2+os.sep+'POSCAR').structure
  if (material1_st!=material2_st): #get rid of double counting
    v_material1 = np.array(ssf.featurize(material1_st))
    v_material2 = np.array(ssf.featurize(material2_st))
    distance = np.linalg.norm(v_material1-v_material2)
    
    
    if distance <= dissimilarity:
          print("SIMILARITY DETECTED!\n"+material1+"("+mpid1+") = "+material2+"("+mpid2+") @ "+"distance=",distance)
          #df.append({'MP_id1':mpid1,'material1':material1,'spg1':spg1,'MP_id2':mpid2,'material2':material2,'spg2':spg2,'distance':distance}, ignore_index=True)
                  
          mpid1_list.append(mpid1)
          mpid2_list.append(mpid2)
          material1_list.append(material1)
          material2_list.append(material2)
          spg1_list.append(spg1)
          spg2_list.append(spg2)
          distance_list.append(distance)
   
        
        
  return mpid1_list,material1_list,spg1_list,mpid2_list,material2_list,spg2_list,distance_list         
     
          
   
if __name__ == "__main__":
    
  #looping over the materials\
  args = []
  for i in range(len(data)):
    for j in range(len(data)):
      mpid1=data.MP_id.iloc[i]
      mpid2=data.MP_id.iloc[j]
      material1=data.pretty_formula.iloc[i]
      material2=data.pretty_formula.iloc[j]
      spg1=data.spg.iloc[i]
      spg2=data.spg.iloc[j]   
      args.append([mpid1,mpid2,material1,material2,spg1,spg2])
      
      
  p = Pool(procs)
  result = p.map(match,args)
  for it in range(len(result)):
    if result[it][0]:  
      df=df.append({'MP_id1':result[it][0][0],'material1':result[it][1][0],'spg1':result[it][2][0],'MP_id2':result[it][3][0],'material2':result[it][4][0],'spg2':result[it][5][0],'distance':result[it][6][0]}, ignore_index=True)
  
  #store the similar materials in a Excel spreadsheet                
  df.to_excel("similar_structures_1000.xlsx",index=False)
  print("Done.")
  
