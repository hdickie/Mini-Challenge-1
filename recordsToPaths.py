# -*- coding: utf-8 -*-
"""
Created on Mon May 29 11:20:35 2017

@author: Hume Dickie
"""

import csv, os, re, numpy as np
from datetime import datetime as dt
from PIL import Image, ImageEnhance, ImageDraw
import random


os.chdir("C:/Users/Hume Dickie/Desktop/Github/Mini-Challenge-1/data/")

writeVisits = True
writePaths = True
writedfEntries = True

mapAbbrev = {"entrance0" : "E0",
             "entrance1" : "E1",
             "entrance2" : "E2",
             "entrance3" : "E3",
             "entrance4" : "E4",
             "camping0" : "C0",
             "camping1" : "C1",
             "camping2" : "C2",
             "camping3" : "C3",
             "camping4" : "C4",
             "camping5" : "C5",
             "camping6" : "C6",
             "camping7" : "C7",
             "camping8" : "C8",
             "general-gate0" : "GG0",
             "general-gate1" : "GG1",
             "general-gate2" : "GG2",
             "general-gate3" : "GG3",
             "general-gate4" : "GG4",
             "general-gate5" : "GG5",
             "general-gate6" : "GG6",
             "general-gate7" : "GG7",
             "general-gate8" : "GG8",
             "ranger-stop0" : "R0",
             "ranger-stop1" : "R1",
             "ranger-stop2" : "R2",
             "ranger-stop3" : "R3",
             "ranger-stop4" : "R4",
             "ranger-stop5" : "R5",
             "ranger-stop6" : "R6",
             "ranger-stop7" : "R7",
             "gate0" : "G0",
             "gate1" : "G1",
             "gate2" : "G2",
             "gate3" : "G3",
             "gate4" : "G4",
             "gate5" : "G5",
             "gate6" : "G6",
             "gate7" : "G7",
             "gate8" : "G8",
             "ranger-base" : "B"
             }
             
nodeIndex = {"E0" : 0,
             "E1" : 1,
             "E2" : 2,
             "E3" : 3,
             "E4" : 4,
             "C0" : 5,
             "C1" : 6,
             "C2" : 7,
             "C3" : 8,
             "C4" : 0,
             "C5" : 10,
             "C6" : 11,
             "C7" : 12,
             "C8" : 13,
             "GG0" : 14,
             "GG1" : 15,
             "GG2" : 16,
             "GG3" : 17,
             "GG4" : 18,
             "GG5" : 19,
             "GG6" : 20,
             "GG7" : 21,
             "GG8" : 22,
             "R0" : 23,
             "R1" : 24,
             "R2" : 25,
             "R3" : 26,
             "R4" : 27,
             "R5" : 30,
             "R6" : 31,
             "R7" : 32,
             "G0" : 33,
             "G1" : 34,
             "G2" : 35,
             "G3" : 36,
             "G4" : 37,
             "G5" : 38,
             "G6" : 39,
             "G7" : 40,
             "G8" : 41,
              "B" : 42
             }

class VisitRecord:    
    def __init__(self,time,gate,visitorId,neverEntered):
        self.times = [time]
        self.path = [gate]
        self.visitorId = visitorId
        self.neverEntered = neverEntered
        
    def addObservation(self,time,gate):
        self.times.append(time)
        self.path.append(gate)
        
    def toString(self):
        #assert len(self.path) == len(self.times)
        returnValue = self.visitorId + "; "
        for i in range(0,len(self.path)):
            if (i == (len(self.path) - 1)):
                returnValue += str(self.times[i]) + ": " + self.path[i] + "\n"
            else:
                returnValue += str(self.times[i]) + ": " + self.path[i] + ", "
        return returnValue
        
    def pathString(self):
        pathString = self.visitorId + "; "
        pathString += str(self.times[0]) + "; "
        pathString += self.path[0] +" "        
        
        #compute time deltas
        timeDeltas = []
        for i in range(1,len(self.times)):
            delta = str(self.times[i] - self.times[i-1])
            timeDeltas.append(delta)
        
        for i in range(0,len(timeDeltas)):
            pathString += str(timeDeltas[i]) + " "
            pathString += self.path[i+1] + " "
            
        pathString = pathString.strip()
        pathString += "\n"
        return pathString
        
    #hitting max line width in .txt files made name abbrev. necessary
    def asDataFrameEntry(self):
        pathString = self.visitorId + ";"
        pathString += str(self.times[0]) + ";"
        pathString += mapAbbrev[self.path[0]] +";"        
        
        #compute time deltas
        timeDeltas = []
        for i in range(1,len(self.times)):
            delta = str(self.times[i] - self.times[i-1])
            timeDeltas.append(delta)
        
        for i in range(0,len(timeDeltas)-1):
            pathString += str(timeDeltas[i]) + ";"
            pathString += mapAbbrev[self.path[i+1]] + ";"
                
        #print(self.visitorId)
        #print(self.path)
        #print(self.times)
        pathString += str(timeDeltas[len(timeDeltas)-1]) +";"
        pathString += mapAbbrev[self.path[len(timeDeltas)]]
        
        pathString += "\n"
        return pathString
        
    def asMatrix(self):
        matrix = np.zeros((40,40))
        
        for i in range(0,len(self.path)-1):
            matrix[nodeIndex[mapAbbrev[self.path[i]]]][nodeIndex[mapAbbrev[self.path[i+1]]]] +=1
            
        return matrix
            
        
def isEntrance(gate):
    t = re.search("entrance[0-4]",gate)
    return hasattr(t,"group")
    
#True = in park, False = has left park. keys are strings and vals are bool
activeCars = {}
#keys are car.id strings and val are lists of VisitRecords
records = {}
#keeps track of place in list for each car in records
numVisits = {}
        

lines = []
with open('sensor.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        lines.append(row)


place = 0
for line in lines[1:]:
        place = place + 1
        timestamp = dt.strptime(line[0],"%Y-%m-%d %H:%M:%S")
        carId = line[1]
        carType = line[2]
        gate = line[3]
        
        is_entrance = isEntrance(gate)
        if carId not in records:
            records[carId] = [VisitRecord(timestamp,gate,carId,is_entrance)]
            activeCars[carId] = True
            numVisits[carId] = 0
        else:
            if (is_entrance and activeCars[carId]):
                #car is leaving
                records[carId][numVisits[carId]].addObservation(timestamp,gate)
                numVisits[carId] +=1
            if (is_entrance and not activeCars[carId]):
                records[carId].append(VisitRecord(timestamp,gate,carId,False))
            if (is_entrance): 
                activeCars[carId] = not activeCars[carId] 
            
            if (not is_entrance):
                records[carId][numVisits[carId]].addObservation(timestamp,gate)
                
                    
                
                
                
                
###plotPaths                
                
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

#there is actually research on whether to jitter the beginning or end. I think
# it's beginning
def plotPath(visRec,imgdraw):
    path = visRec.path
    nodes = []
    for i in range(0,len(path)):
        nodes.append(path[i])
    
    #rgb
    c0 = [0, 255, 0]
    c1 = [255, 0, 0]
    
    
    place = 0
    for i in range(0,len(nodes)-1):
        #point        
        x0 = gateCoords[mapAbbrev[nodes[i]]][0]
        y0 = gateCoords[mapAbbrev[nodes[i]]][1]
        x1 = gateCoords[mapAbbrev[nodes[i+1]]][0]
        y1 = gateCoords[mapAbbrev[nodes[i+1]]][1]
          
        
        scr = abs(int((c1[0]-c0[0])*(float(i)/(len(nodes)-1))))
        scg = 255 - abs(int((c1[1]-c0[1])*(float(i)/(len(nodes)-1))))
        scb = abs(int((c1[2]-c0[2])*(float(i)/(len(nodes)-1))))
        
        j1 = random.randint(3,10)
        j2 = random.randint(3,10)
        
        imgdraw.line((x0 + j1,y0 + j2,x1,y1), fill = (scr,scg,scb,128), width = 1)
        
        tx = x0 + j1
        ty = y0 + j2
        
        imgdraw.text((tx,ty),str(place))
        place += 1
        
        if (i == len(nodes) - 2): #draw last label
            x = gateCoords[mapAbbrev[nodes[len(nodes)-1]]][0]
            y = gateCoords[mapAbbrev[nodes[len(nodes)-1]]][1]
            imgdraw.text((x,y),str(place))
        
    ###new alg
    #for i in range(0,len(nodes)-1):
    #    print i 


os.chdir("C:/Users/Hume Dickie/Desktop/Github/Mini-Challenge-1/img")

try:
    parkmap = Image.open("labeled-map.jpg")
    parkmap.load()
except:
    print "failed to open image"
    
contrastModifier = ImageEnhance.Contrast(parkmap) 

faded = contrastModifier.enhance(0.1)
plot = ImageDraw.Draw(faded)

#weird car "20155705025759-63"
# a ranger "20153722123707-242"
plotPath(records["20155705025759-63"][0],plot)

faded.show()                
                
                
                
                
                
###plotPaths                
                
                
                
                
#what is the longest path? 70

#print results!
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