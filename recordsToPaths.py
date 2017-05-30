# -*- coding: utf-8 -*-
"""
Created on Mon May 29 11:20:35 2017

@author: Hume Dickie
"""

import csv
import os
import re
from datetime import datetime as dt

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