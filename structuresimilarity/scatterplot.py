#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
import pandas

#importing data from excel file
data_read = pandas.read_excel('similar_structures_test.xlsx')
data=data_read.dropna()

G = nx.Graph()
#pos=nx.spring_layout(G)

G.add_node(0)
for i in range(len(data.MP_id1)):
    if data.distance[i]<0.2:
      G.add_edge(0,i, weight=data.distance[i],color='green')
    else:
      G.add_edge(0,i, weight=data.distance[i],color='grey')

val_map={0:0}
values = [val_map.get(node, 0.9) for node in G.nodes()]

#edge color
edges = G.edges()
colors = [G[u][v]['color'] for u,v in edges]   

nx.draw(G,node_size=3,width=0.5,edges=edges,edge_color=colors,node_color=values,cmap=plt.get_cmap('rainbow'))
plt.draw()
plt.savefig('scatter_circle.png')
plt.show()

