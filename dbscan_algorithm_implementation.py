# -*- coding: utf-8 -*-
"""DBSCAN Algorithm implementation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1AamZ4yQULvzAUFCYERumoih7GLsuoMcS
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import DBSCAN


# Define a function to generate clusters
def Generate_cluster_fun(No_of_clusters, pts_minmax=(1, 100), x_mult=(1, 4), y_mult=(1, 3),
                x_off=(0, 50), y_off=(0, 50)):
    # Initialize some empty lists to receive cluster member positions
    x_cluster = []
    y_cluster = []
    # Genereate random values given parameter ranges
    no_of_points = np.random.randint(pts_minmax[0], pts_minmax[1], No_of_clusters)
    x_mul = np.random.randint(x_mult[0], x_mult[1], No_of_clusters)
    y_mul = np.random.randint(y_mult[0], y_mult[1], No_of_clusters)
    x_offsets = np.random.randint(x_off[0], x_off[1], No_of_clusters)
    y_offsets = np.random.randint(y_off[0], y_off[1], No_of_clusters)

    # Generate random clusters given parameter values
    for idx, npts in enumerate(no_of_points):
        xpts = np.random.randn(npts) * x_mul[idx] + x_offsets[idx]
        ypts = np.random.randn(npts) * y_mul[idx] + y_offsets[idx]
        x_cluster.append(xpts)
        y_cluster.append(ypts)

    # Return cluster positions
    return x_cluster, y_cluster


# Generate some clusters!
No_of_clusters = 50
x_cluster, y_cluster = Generate_cluster_fun(No_of_clusters)
# Convert to a single dataset in OpenCV format
data = np.float32((np.concatenate(x_cluster), np.concatenate(y_cluster))).transpose()
# Define max_distance (eps parameter in DBSCAN())
max_distance = 1
db = DBSCAN(eps=max_distance, min_samples=10).fit(data)
# Extract a mask of core cluster members
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
# Extract labels (-1 is used for outliers)
labels = db.labels_
No_of_clusters = len(set(labels)) - (1 if -1 in labels else 0)
unique_labels = set(labels)

# Plot up the results!
min_x = np.min(data[:, 0])
max_x = np.max(data[:, 0])
min_y = np.min(data[:, 1])
max_y = np.max(data[:, 1])

fig = plt.figure(figsize=(12, 6))
plt.subplot(121)
plt.plot(data[:, 0], data[:, 1], 'ko')
plt.xlim(min_x, max_x)
plt.ylim(min_y, max_y)
plt.title('Input Data', fontsize=20)

plt.subplot(122)

colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = data[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=7)

    xy = data[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=3)
plt.xlim(min_x, max_x)
plt.ylim(min_y, max_y)
plt.title('DBSCAN: %d clusters found by the algorithm' % No_of_clusters, fontsize=20)
fig.tight_layout()
plt.subplots_adjust(left=0.03, right=0.98, top=0.9, bottom=0.05)