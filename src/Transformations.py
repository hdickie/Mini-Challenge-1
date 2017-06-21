# -*- coding: utf-8 -*-
"""
Created on Mon May 29 11:20:35 2017

@author: Hume Dickie
"""

import csv
import time
from datetime import datetime as dt

from IndividualRecord import IndividualRecord
from ParkUtils import isEntranceOrBase, nodeIndex

from GroupHangout import GroupHangout

def rowsToIndiRecords(fileName):
    
    #True = in park, False = has left park. keys are strings and vals are bool
    activeCars = {}
    
    #keys are car.id strings and val are lists of VisitRecords
    records = {}
    
    #keeps track of place in list for each car in records
    numVisits = {}
    
    lines = []
    with open(fileName) as csvfile:
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
        
        is_entrance = isEntranceOrBase(gate)
        if carId not in records:
            records[carId] = [IndividualRecord(timestamp,gate,carId,carType)]
            activeCars[carId] = True
            numVisits[carId] = 0
        else:
            if (is_entrance and activeCars[carId]):
                #car is leaving
                records[carId][numVisits[carId]].addObservation(timestamp,gate)
                numVisits[carId] +=1
            if (is_entrance and not activeCars[carId]):
                records[carId].append(IndividualRecord(timestamp,gate,carId,False))
            if (is_entrance): 
                activeCars[carId] = not activeCars[carId] 
            
            if (not is_entrance):
                records[carId][numVisits[carId]].addObservation(timestamp,gate)
    
    return records
    
def indiRecordsToCampRecords(indiRecordsLines):
    campRecs = [] #output container    
    
    for line in indiRecordsLines[1:]:
        for disp in range(0,int(line[3])-1):
            
            #if they were there longer than a day
            if (int(line[6 + disp*2][0:len(line[6 + disp*2])-2]) > 60*60*24/2) :
                assert (line[6 + disp*2 - 1] == line[6 + disp*2 + 1])  #enter and exit gate match
                oline = line[0] + "," #car.id
                oline += line[1] + "," #car.type
                
                parkEntranceTimestamp = time.mktime(dt.strptime(line[2],"%Y-%m-%d %H:%M:%S").timetuple())         
                
                entranceToCampTime = 0
                for i in range(0,disp):
                    entranceToCampTime += int(line[6 + disp*2][0:len(line[6 + disp*2])-2])
                campEntranceTimeUnix = parkEntranceTimestamp + entranceToCampTime
                campEntranceTime = dt.fromtimestamp(campEntranceTimeUnix)
                    
                oline += str(campEntranceTime) + ","
                oline += str(int(campEntranceTimeUnix)) + "," #startTimestamp
                oline += line[6 + disp*2 - 1] + "," #gaten.name
                
                duration = line[6 + disp*2][0:len(line[6 + disp*2])-2]
                oline += duration +";" #duration
                
                estimatedEnd = dt.fromtimestamp((campEntranceTimeUnix + float(duration)))
                oline += str(campEntranceTimeUnix + float(duration)) + "," #
                oline += str(estimatedEnd) + "\n"
                campRecs.append(oline)
                
    return campRecs
    
def sortedCampRecsToGroupHangouts(sortedLines):
    
    pastHangouts = {}
    
    for key in nodeIndex:
        pastHangouts[key] = []
    
    activeCamps = {}
      
    currentTime = -1
    for line in sortedLines[1:]:
        #rowNum = lin[0]
        carId = line[1]
        startDatetime = line[2]
        startTime = int(line[3])
        gate = line[4]
        duration = int(line[5])
        endTime = int(line[6])
        endDatetime = line[7]
        
        if (not (currentTime <= startTime)):
            print currentTime, startTime
        assert currentTime <= startTime
        currentTime = startTime
        
        #a vehicle has arrived at campsite
        if (gate not in activeCamps):
            newHangout = GroupHangout(carId,startTime,gate)
            activeCamps[gate] = newHangout
            
        #a non-first camper has arrived
        elif (not activeCamps[gate].containsCamper(carId)):
            activeCamps[gate].addCamper(carId,startTime)
            
        #oh no... campers dont leave! They just time out!
        #a camper is leaving
        #elif (activeCamps[gate].containsCamper(carId)):
        #    print "LEAVING ", gate, carId
        #    activeCamps[gate].removeCamper(carId,)
        #    
        #    if (activeCamps[gate].size == 0):
        #        pastHangouts[gate].append(activeCamps[gate])
        #        activeCamps.remove(gate)
        #else:
        #    print "else block"
    
    for g in activeCamps:
        print activeCamps[g].gate," | SIZE =",activeCamps[g].size