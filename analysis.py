# -*- coding: utf-8 -*-
"""
Created on Tue May 23 22:17:20 2017

@author: Hume Dickie
"""

import os
import csv
from datetime import datetime

#for heatmap
import matplotlib.pyplot as plt
import numpy as np

os.chdir('C:\\Users\\Hume Dickie\\Desktop\\Github\\Mini-Challenge-1\\')

lines = []
with open('Lekagul Sensor Data.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        lines.append(row)

datetime_objs = []
for i in range(1,len(lines)):
    new_datetime = datetime.strptime(lines[i][0],"%Y-%m-%d %H:%M:%S")
    datetime_objs.append(new_datetime)

elementList = []
for i in range(0,len(datetime_objs)):
    curr = datetime_objs[i]
    elementList.append([curr.year,curr.month,curr.day,curr.hour,curr.minute,curr.second])
    
day = []
hour = []
minute = []
for i in range(0,len(datetime_objs)):
    curr = datetime_objs[i]
    day.append(curr.day)
    hour.append(curr.hour)
    minute.append(curr.minute)

 
# Create heatmap
heatmap, xedges, yedges = np.histogram2d(day, hour, bins=(31,24))
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
 
#Specify size
# Get current size
fig_size = plt.rcParams["figure.figsize"]

 
# Set figure width to 12 and height to 9
l = 8
fig_size[0] = l
fig_size[1] = l
plt.rcParams["figure.figsize"] = fig_size 
 
# Plot heatmap
plt.clf()
plt.title('Lekagul Sensor Data: Hour vs Day')
plt.ylabel('Hour')
plt.xlabel('Day')
plt.imshow(heatmap, extent=extent)
plt.show()





