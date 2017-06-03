# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 18:01:59 2017

@author: Hume Dickie
"""

import numpy as np
from ParkUtils import mapAbbrev, nodeIndex

class VisitRecord:    
    def __init__(self,time,gate,visitorId,neverEntered):
        self.times = [time]
        self.path = [gate]
        self.visitorId = visitorId
        self.neverEntered = neverEntered
        
    #should i change toString to this?
    #def __str__(self):  
        
    #value returned is in seconds
    def getTotalTime(self):
        return str((self.times[len(self.times)-1] - self.times[0]).total_seconds())
        
    #used to build paths from rows
    def addObservation(self,time,gate):
        self.times.append(time)
        self.path.append(gate)
        
    def toString(self):
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
        pathString = self.visitorId + ";"               #id
        pathString += str(self.neverEntered) + ";"      #neverEntered
        pathString += str(self.times[0]) + ";"          #enterTime
        pathString += str(len(self.path)) + ";"         #pathLength
        pathString += self.getTotalTime() + ";"         #totalTime
        pathString += mapAbbrev[self.path[0]] +";"      #startGate
        
        #compute time deltas
        timeDeltas = []
        for i in range(1,len(self.times)):
            delta = str(self.times[i] - self.times[i-1])
            timeDeltas.append(delta)
        
        for i in range(0,len(timeDeltas)-1):
            pathString += str(timeDeltas[i]) + ";"
            pathString += mapAbbrev[self.path[i+1]] + ";"
                
        pathString += str(timeDeltas[len(timeDeltas)-1]) +";"
        pathString += mapAbbrev[self.path[len(timeDeltas)]]
        
        pathString += "\n"
        return pathString
        
    def asMatrix(self):
        matrix = np.zeros((40,40))
        
        for i in range(0,len(self.path)-1):
            matrix[nodeIndex[mapAbbrev[self.path[i]]]][nodeIndex[mapAbbrev[self.path[i+1]]]] +=1
            
        return matrix