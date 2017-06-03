# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 19:48:10 2017

@author: Hume Dickie
"""

from config import imgDirectory, outputDirectory, mapName
from config import writeVisits, writePaths, writedfEntries

from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import random, os
from ParkUtils import mapAbbrev, gateCoords

#Plots
def plotPath(visRec):
    #color scale end points
    c0 = (0,255,0,0)    #first color
    c1 = (255,0,0,0)    #second color
    
    os.chdir(imgDirectory)
    
    try:
        parkmap = Image.open(mapName)
    except:
        print "Unable to load image"
    
    #fade the map to make the paths easier to see
    contrast = ImageEnhance.Contrast(parkmap)
    faded = contrast.enhance(0.15)
    imgdraw = ImageDraw.Draw(faded)
    
    #draw lines
    for i in range(0,len(visRec.path)-1):
        
        n0 = mapAbbrev[visRec.path[i]]
        n1 = mapAbbrev[visRec.path[i+1]]
        
        iR = int((c1[0] - c0[0])*(float(i)/(len(visRec.path)-1)))
        iG = int((c1[1] - c0[1])*(float(i)/(len(visRec.path)-1)))
        iB = int((c1[2] - c0[2])*(float(i)/(len(visRec.path)-1)))
        ia = int((c1[3] - c0[3])*(float(i)/(len(visRec.path)-1)))
        
        if (iR < 0) : iR = 255 + iR
        if (iG < 0) : iG = 255 + iG
        if (iB < 0) : iB = 255 + iB
        if (ia < 0) : ia = 255 + ia
        
        #jitter
        j1 = random.randint(-25,25)
        j2 = random.randint(-25,25)
        
        x0 = gateCoords[n0][0] + j1  
        y0 = gateCoords[n0][1] + j2
        x1 = gateCoords[n1][0] + j1
        y1 = gateCoords[n1][1] + j2
        
        imgdraw.line((x0,y0,x1,y1),
                      fill=(iR,iG,iB,ia), 
                      width = 1)
                      
        fontsize = 20
                      
        font = ImageFont.truetype("arial.ttf", fontsize)                      
                      
        imgdraw.text((x1,y1),str(i),font = font)
    
    return faded
    
def writeOutputFiles(records):
    os.chdir(outputDirectory)
    
    if (writeVisits):
        visits = open("visits.txt",'w')
        for key in records:
            for v in records[key]:
                visits.write(v.toString())
        visits.close()
    
    if (writePaths):
        paths = open("paths.txt",'w')
        for key in records:
            for p in records[key]:
                paths.write(p.pathString())
        paths.close()
        
    if (writedfEntries):
        asDF = open("abbrev-paths.txt",'w')
        for key in records:
            for d in records[key]:
                asDF.write(d.asDataFrameEntry())
        asDF.close()
        
    #if (actCars):
    #    cars_in_park = open("activeCars.txt",'w')
    #    for key in activeCars:
    #        if (activeCars[key] == True):
    #            cars_in_park.write(key + "\n")