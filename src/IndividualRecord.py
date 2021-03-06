# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 18:01:59 2017

@author: Hume Dickie
"""

import numpy as np
from ParkUtils import mapAbbrev, nodeIndex

class IndividualRecord:    
    def __init__(self,time,gate,visitorId,carType):
        self.times = [time]
        self.path = [gate]
        self.visitorId = visitorId
        self.carType = carType
        
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
            delta = (self.times[i] - self.times[i-1])
            timeDeltas.append(delta)
        
        for i in range(0,len(timeDeltas)):
            pathString += str(timeDeltas[i].total_seconds()) + " "
            pathString += self.path[i+1] + " "
            
        pathString = pathString.strip()
        pathString += "\n"
        return pathString
        
    def visitedRangerStop(self):
        rangerStops = ["R0","R1""R2","R3","R4","R5","R6","R7","B"]
        
        return not set(rangerStops).isdisjoint(self.path)
        
    #hitting max line width in .txt files made name abbrev. necessary
    def asDataFrameEntry(self):
        pathString = self.visitorId + ";"               #id
        pathString += str(self.carType) + ";"      #carType
        pathString += str(self.times[0]) + ";"          #enterTime
        pathString += str(len(self.path)) + ";"         #pathLength
        pathString += self.getTotalTime() + ";"         #totalTime
        pathString += mapAbbrev[self.path[0]] +";"      #startGate 
        
        
        #compute time deltas
        timeDeltas = []
        for i in range(1,len(self.times)):
            delta = self.times[i] - self.times[i-1]  
            timeDeltas.append(delta)
        
        for i in range(0,len(timeDeltas)-1):
            #pathString += str(self.times[i+1]) + ";"
            pathString += str(timeDeltas[i].total_seconds()) + ";"
            pathString += mapAbbrev[self.path[i+1]] + ";"
                
        pathString += str(timeDeltas[len(timeDeltas)-1].total_seconds()) +";"
        pathString += mapAbbrev[self.path[len(timeDeltas)]]
        
        pathString += "\n"
        return pathString
        
    def asMatrix(self):
        matrix = np.zeros((40,40))
        
        for i in range(0,len(self.path)-1):
            matrix[nodeIndex[mapAbbrev[self.path[i]]]][nodeIndex[mapAbbrev[self.path[i+1]]]] +=1
            
        return matrix
    