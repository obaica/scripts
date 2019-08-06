#!/usr/bin/env python3
"""
This network plot uses the 7 crystal systems as categories for the matched entries.
"""

import matplotlib.pyplot as plt
import networkx as nx
import pandas
import numpy as np
import matplotlib.patches as mpatches
from collections import Counter
import json

#importing data from excel file
data_read = pandas.read_excel('similar_structures.xlsx')
data=data_read.dropna()

#importing data from excel file
data_read2 = pandas.read_excel('similar_structures.xlsx')
data2=data_read2.dropna()
# dropping duplicte values 
data2.drop_duplicates(subset =["MP_id1","MP_id2"],keep ="first",inplace=True )   
spacegrouptypes1=np.unique(np.array(data2.spg1))
spacegrouptypes2=np.unique(np.array(data2.spg2))
spacegrouptypes=np.unique(np.concatenate((spacegrouptypes1,spacegrouptypes2)))

#importing Complete File
#importing data from excel file
data_read3 = pandas.read_excel('All.xlsx')
data3=data_read3.dropna()
# dropping duplicte values 
data3.drop_duplicates(subset ="MP_id",keep ="first",inplace=True ) 

colorpallette=['purple','b','g','c','y','m','orange']
bravaislattices=['Triclinic','Monoclinic','Orthorhombic','Tetragonal','Trigonal','Hexagonal','Cubic']

color_dic = dict(zip(bravaislattices,colorpallette))

#create nodes only with similarity weights for edge distance
G = nx.Graph()
for i in range(len(data.MP_id1)):
  if data.distance[i]<0.5:
    G.add_edge(data.MP_id1.iloc[i],data.MP_id2.iloc[i], weight=data.distance.iloc[i]) #color='grey')
  
#create nodes
#G = nx.Graph()
#for i in range(len(data.MP_id1)):
#    if data.spg1.iloc[i] != data.spg2.iloc[i]:
#      G.add_edge(data.MP_id1.iloc[i],data.MP_id2.iloc[i], weight=data.distance.iloc[i],color='red')
#    else:
#      G.add_edge(data.MP_id1.iloc[i],data.MP_id2.iloc[i], weight=data.distance.iloc[i],color='grey')
#      
#create nodes color with similarity threshhold for edges
#G = nx.Graph()
#for i in range(len(data.MP_id1)):
#    if data.distance.iloc[i] < 0.3:
#      G.add_edge(data.MP_id1.iloc[i],data.MP_id2.iloc[i], weight=data.distance.iloc[i],color='red')
#    else:
#      G.add_edge(data.MP_id1.iloc[i],data.MP_id2.iloc[i], weight=data.distance.iloc[i],color='grey')
      
      

G_array=np.array(G.nodes)  

#Get spacegroup number as a list
G_spg=[]
for G_counter in G_array:
    G_spg.append(data3[data3.MP_id==G_counter].spg)    
G_spg_num = []
for G_spg_count in range(len(G_spg)):
    G_spg_num.append(int(G_spg[G_spg_count].values[0])) #The number itself
    
G_bravais=[]
for G_spg_num_iter in G_spg_num:
    if G_spg_num_iter<3:
      G_bravais.append('Triclinic')
    elif G_spg_num_iter<16:
      G_bravais.append('Monoclinic')
    elif G_spg_num_iter<75:
      G_bravais.append('Orthorhombic')  
    elif G_spg_num_iter<143:
      G_bravais.append('Tetragonal')    
    elif G_spg_num_iter<168:
      G_bravais.append('Trigonal') 
    elif G_spg_num_iter<195:
      G_bravais.append('Hexagonal')    
    else:
      G_bravais.append('Cubic')

G_colors=[]    
for G_bravais_val in G_bravais:
    G_colors.append(color_dic[G_bravais_val])
    
#weights for line widthdata.distance.iloc[i]
#weights = [G[u][v]['weight'] for u,v in G.edges()]
#in the next line do width=weights    

#edge color
edges = G.edges()
#colors = [G[u][v]['color'] for u,v in edges]    

#plt.figure(figsize=(13,9))    
dx = nx.degree(G)   
#pos = nx.spring_layout(G,scale=1,k=0.075,weight='weight')

#getting weights as edge colors
edges,weights = zip(*nx.get_edge_attributes(G,'weight').items())


#loading previous positions
rf = open('positions.json','r')
test = json.load(rf)
rf.close()


nx.draw(G,pos=test,node_color=G_colors,edgelist=edges,edge_color=weights,edge_cmap=plt.cm.Reds,width=0.4,node_size=[8*items[1] for items in dx])#,with_labels=True,font_size=10)
#text = nx.draw_networkx_labels(G,test)

#legend
patches=[]
for ii in range(len(color_dic)):
    patches.append( mpatches.Patch(color=colorpallette[ii],label=bravaislattices[ii]))
#plt.legend(handles=patches,fontsize=12)

    
#count items
stats = Counter(G_bravais)   

#stat data
#props = dict(boxstyle='round',alpha=0)
#y=-0.95
#for key,value in stats.items():
#    plt.text(0.7,y,'%s:%s'%(key,value),bbox=props,fontsize=15)
#    y+=0.1
    
plt.tight_layout()

plt.draw()
plt.savefig('scatter_network_bravais.pdf',dpi=500)


plt.show()



