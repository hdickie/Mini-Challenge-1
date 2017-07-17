# -*- coding: utf-8 -*-
"""
Created on Sun Jul 16 13:20:15 2017

@author: Hume Dickie
"""

import os, csv, config

#PopulationMonitor.py
class PopulationMonitor:
    def __init__(self):
        prevDir = os.getcwd()
        os.chdir(config.outputDirectory)

        lines = []
        camps = {}
        try:
            with open("campsite-population-time-series.txt",'r') as csvfile:
                reader = csv.reader(csvfile,delimiter=",")
                for row in reader:
                    lines.append(row)
                    
                    time = row[0]                    
                    gate = row[1]
                    #carID = row[2]
                    pop = row[3]
                    
                    if gate not in camps:
                        camps[gate] = [(time,pop)]
                    else:
                        camps[gate].append((time,pop))
        except:
            print "Failed to open campsite-population-time-series.txt. Does that file exist?"
            
        for k in camps.keys():
            camps[k].sort(key = lambda x: x[0])
        
        self.camps = camps
        os.chdir(prevDir)
        
    def getExtent(self):
        for k in ("C0","C1","C2","C3","C4","C5","C6","C7","C8"):
            currCampList = self.camps[k]
            print k
            print "time of first record", currCampList[0][0]
            print "time of last record", currCampList[len(currCampList)-1][0]

    def getCampCounts(self,integerTime):
        out = {}        
        
        for k in ("C0","C1","C2","C3","C4","C5","C6","C7","C8"):
            currCampList = self.camps[k]
            if integerTime < int(currCampList[0][0]): #if time is before first record
                out[k] = 0
                #print k, "before first record"
            elif integerTime >= int(currCampList[len(currCampList)-1][0]): #if time is after last record
                out[k] = currCampList[len(currCampList)-1][1]
                #print k, "after last record"
            else:
                #print k, "value exists"
                for i in range(0,len(currCampList)):
                    if int(currCampList[i][0]) <= integerTime < int(currCampList[i+1][0]): #if found before and after record
                        #print k, "      value sucessfully found"
                        out[k] = currCampList[i][1]
                            
        #print integerTime, out.keys()
        return (out["C0"],out["C1"],out["C2"],out["C3"],out["C4"],out["C5"],out["C6"],out["C7"],out["C8"])