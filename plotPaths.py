# -*- coding: utf-8 -*-
"""
Created on Tue May 30 12:20:30 2017

@author: Hume Dickie
"""

#plotPaths

import os
from PIL import Image, ImageEnhance, ImageDraw
import csv

gateCoords = {"E0" : (310,69),
              "E1" : (90,331),
              "E2" : (898,430),
              "E3" : (566,818),
              "E4" : (688,903),
              "C0" : (259,205),
              "C1" : (634,248),
              "C2" : (220,318),
              "C3" : (225,335),
              "C4" : (240,436),
              "C5" : (101,595),
              "C6" : (736,869),
              "C7" : (889,710),
              "C8" : (898,240),
              "GG0" : (542,50),
              "GG1" : (319, 129),
              "GG2" : (511,161),
              "GG3" : (913,273),
              "GG4" : (344,482),
              "GG5" : (609,546),
              "GG6" : (668,673),
              "GG7" : (322,704),
              "R0" : (440,84),
              "R1" : (98,121),
              "R2" : (395,174),
              "R3" : (727,224),
              "R4" : (93,467),
              "R5" : (740,581),
              "R6" : (606, 722),
              "R7" : (494, 744),
              "G0" : (312,167),
              "G1" : (288,220),
              "G2" : (122,270),
              "G3" : (732, 297),
              "G4" : (805,559),
              "G5" : (644,716),
              "G6" : (571, 740),
              "G7" : (477,785),
              "G8" : (678, 886),
              "B" : (628,856)
              }

def plotPath(path,imgdraw):
    pathLength = (len(path) - 1)/2
    nodes = []
    for i in range(0,pathLength):
        nodes.append(path[i*2 + 2])
    
    for i in range(0,len(nodes)-1):
        x0 = gateCoords[nodes[i]][0]
        y0 = gateCoords[nodes[i]][1]
        x1 = gateCoords[nodes[i+1]][0]
        y1 = gateCoords[nodes[i+1]][1]
        
        imgdraw.line((x0,y0,x1,y1), fill = 128, width = 3)

os.chdir("C:/Users/Hume Dickie/Desktop/Github/Mini-Challenge-1/data")

paths = []
with open("abbrev-paths.txt",'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
        paths.append(row)

os.chdir("C:/Users/Hume Dickie/Desktop/Github/Mini-Challenge-1/img")

try:
    parkmap = Image.open("labeled-map.jpg")
    parkmap.load()
except:
    print "failed to open image"
    
contrastModifier = ImageEnhance.Contrast(parkmap) 

faded = contrastModifier.enhance(0.1)
plot = ImageDraw.Draw(faded)


plotPath(paths[12],plot)

faded.show()