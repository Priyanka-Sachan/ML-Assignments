# -*- coding: utf-8 -*-
"""ai-assignment-2

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kVoB_YRDQ8_bdNQc-0lC69Z43z2U7SWb
"""

# Commented out IPython magic to ensure Python compatibility.
# Import libraries and packages
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

# scaling 
from sklearn.preprocessing import StandardScaler

# KMeans clustering 
from sklearn.cluster import KMeans
# DBSCAN clustering
from sklearn.cluster import DBSCAN

# silhouette score
from sklearn.metrics import silhouette_score

# Read csv file
blob_df = pd.read_csv(f'data/cluster_blobs.csv')
circle_df = pd.read_csv(f'data/cluster_circles.csv')
moon_df = pd.read_csv(f'data/cluster_moons.csv')

# Creating a dictionary for dataframes
df={'blob':blob_df,'circle':circle_df,'moon':moon_df}

# Get statistical information
for shape in ['blob','circle','moon']:
  print('\n',shape.upper(),'DATASET')
  print(df[shape].describe())
  print('-------------------------------')

# Scaling data
scaled_df={}
for shape in ['blob','circle','moon']:
  print('\n',shape.upper(),'SCALED DATA')
  scaled=StandardScaler().fit_transform(df[shape])
  scaled_df[shape]=pd.DataFrame(scaled,columns=df[shape].columns)
  print(scaled_df[shape])
  print('------------------------')

dbscan_labels={}
dbscan_clusters={}
print('DBSCAN CLUSTERING')

for shape in ['blob','circle','moon']:
  # Training datset on dbscan model
  dbscan = DBSCAN(eps=0.3, min_samples=10).fit(scaled_df[shape])

  # Get predicted labels
  dbscan_labels[shape] = dbscan.labels_
  # Number of clusters in labels
  dbscan_clusters[shape]=len(set(dbscan_labels[shape])) - (1 if -1 in dbscan_labels[shape] else 0)

  print('\n',shape.upper(),'DATASET EVALUATION')
  print("Estimated number of clusters: %d" % dbscan_clusters[shape])
  print("Silhouette Score: %0.3f" % silhouette_score(scaled_df[shape], dbscan_labels[shape]))
  print('-----------------------------------')

print('CLUSTERING VISUALIZATION')
fig, ax = plt.subplots(1, 3, figsize=(21,6))
id=0

for shape in ['blob','circle','moon']:
  ax[id].scatter(df[shape].iloc[:,0],df[shape].iloc[:,1],c=dbscan_labels[shape], cmap='Paired')
  ax[id].set_title(shape.upper()+' DBSCAN CLUSTERING')
  id+=1

plt.xlabel("X1") # X-axis label
plt.ylabel("X2") # Y-axis label
plt.show() # showing the plot

kmeans_labels={}
print('KMEANS CLUSTERING')

for shape in ['blob','circle','moon']:
  # Training datset on dbscan model
  kmeans = KMeans(n_clusters = dbscan_clusters[shape],random_state = 0).fit(scaled_df[shape])

  # Get predicted labels
  kmeans_labels[shape] = kmeans.labels_

  print('\n',shape.upper(),'DATASET EVALUATION')
  print("Silhouette Score: %0.3f" % silhouette_score(scaled_df[shape], kmeans_labels[shape]))
  print('-----------------------------------')

print('CLUSTERING VISUALIZATION')
fig, ax = plt.subplots(1, 3, figsize=(21,6))
id=0

for shape in ['blob','circle','moon']:
  ax[id].scatter(df[shape].iloc[:,0],df[shape].iloc[:,1],c=kmeans_labels[shape], cmap='Paired')
  ax[id].set_title(shape.upper()+' KMEANS CLUSTERING')
  id+=1

plt.xlabel("X1") # X-axis label
plt.ylabel("X2") # Y-axis label
plt.show() # showing the plot