# -*- coding: utf-8 -*-
"""
Created on Mon May 29 11:20:35 2017

@author: Hume Dickie
"""

import csv
import os
import re

os.chdir("C:/Users/Hume Dickie/Desktop/Github/Mini-Challenge-1/data/")

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
        assert len(self.path) == len(self.times)
        returnValue = self.visitorId + "; "
        for i in range(0,len(self.path)):
            if (i == (len(self.path) - 1)):
                returnValue += self.times[i] + ": " + self.path[i] + "\n"
            else:
                returnValue += self.times[i] + ": " + self.path[i] + ", "
        return returnValue
        
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

for line in lines:
    place = place + 1
    timestamp = line[0]
    carId = line[1]
    carType = line[2]
    gate = line[3]
    if (isEntrance(gate)):
        if carId not in activeCars:
            records[carId] = [VisitRecord(timestamp,gate,carId,False)]
            activeCars[carId] = True    #car is entering
        else:
            if carId not in records:        #test code. replace w error code later
                print("A car has left without entering!")
                print(line)
            if carId in records:
                if carId not in numVisits:
                    records[carId][0].addObservation(timestamp,gate)
                    numVisits[carId] = 0
                else:                   
                    if (activeCars[carId] == False):
                        records[carId].append(VisitRecord(timestamp,gate,carId,False))
                    else:
                        records[carId][numVisits[carId]].addObservation(timestamp,gate)
                    numVisits[carId] = numVisits[carId] + 1
            activeCars[carId] = False   #car is leaving
    else:
        if carId not in activeCars:
            activeCars[carId] = True    #car is entering
            records[carId] = [VisitRecord(timestamp,gate,carId,True)]
        else:
            if carId not in numVisits: #if this is the first visit
                records[carId][0].addObservation(timestamp,gate)
            else:
                records[carId][numVisits[carId]].addObservation(timestamp,gate)
                
                
#print results!
visits = open("visits.txt",'w')
for key in records:
    for v in records[key]:
        visits.write(v.toString())
visits.close()