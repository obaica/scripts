#!/usr/bin/env python3

#This network plot is for all different spacegroups without categorizing them.

import matplotlib.pyplot as plt
import networkx as nx
import pandas
import numpy as np
import matplotlib.patches as mpatches

#importing data from excel file
data_read = pandas.read_excel('similar_structures_test.xlsx')
data=data_read.dropna()

#importing data from excel file
data_read2 = pandas.read_excel('similar_structures_test.xlsx')
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

colorpallette=['r','b','g','c','y','m','k','orange','darkgreen','lightblue','purple']
colormap = []
color_dic = dict(zip(spacegrouptypes,colorpallette))


G = nx.Graph()
for i in range(len(data.MP_id1)):
	G.add_edge(data.MP_id1.iloc[i],data.MP_id2.iloc[i], weight=data.distance.iloc[i])

G_array=np.array(G.nodes)  
G_spg=[]
for G_counter in G_array:
    G_spg.append(data3[data3.MP_id==G_counter].spg)
    
G_spg_num = []
for G_spg_count in range(len(G_spg)):
    G_spg_num.append(int(G_spg[G_spg_count].values[0]))

G_colors=[]    
for G_spg_num_val in G_spg_num:
    G_colors.append(color_dic[G_spg_num_val])
    
plt.figure(figsize=(13,9))

weights = [G[u][v]['weight'] for u,v in G.edges()]
    
dx = nx.degree(G)   
nx.draw(G,node_color=G_colors,node_size=[items[1] for items in dx],width=weights)

patches=[]
for ii in range(len(spacegrouptypes)):
    patches.append( mpatches.Patch(color=colorpallette[ii],label=spacegrouptypes[ii]))

plt.legend(handles=patches)

plt.draw()
plt.savefig('scatter_network.pdf')
plt.show()



