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
        timestamp = dt.strptime(line[0],"%m/%d/%Y %H:%M")
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
                records[carId].append(IndividualRecord(timestamp,gate,carId,carType))
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
                
                print line[2]
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
                oline += duration +"," #duration
                
                estimatedEnd = dt.fromtimestamp((campEntranceTimeUnix + float(duration)))
                oline += str(campEntranceTimeUnix + float(duration)) + ","
                oline += str(estimatedEnd) + "\n"
                campRecs.append(oline)
                
    return campRecs
    
"""
def sortedSingleCampRecsToGroupHangouts(sortedLines):
        
    pastHangouts = []
    maxSizeEver = 0
    
    currentGroup = []
    currentSize = 0
    
    currentTime = -1
    for line in sortedLines[1:]:
        carId = line[1]
        startTime = int(line[3])
        duration = int(line[5])
              
        if carId not in currentGroup:
            currentGroup.append(carId)
            currentSize += 1 
            if (currentSize > maxSizeEver):
                maxSizeEver = currentSize              
        else:
            
            currentSize -= 1
            if (currentSize == 0):
                currentGroup.append(maxSizeEver)
                pastHangouts.append(currentGroup)
                currentGroup = []
                maxSizeEver = 0    
    
    print pastHangouts
    print currentGroup
"""            

#TODO: this algorithm!!!
def sortedCampRecsToGroupHangouts(sortedLines): 
    
    hangouts = {}
    campNames = ["C0","C1","C2","C3","C4","C5","C6","C7","C8"]
    
    for camp in campNames:
        hangouts[camp] = []
      
    currentTime = -1
    for line in sortedLines[1:]:
        #rowNum = lin[0]
        carId = line[1]
        carType = line[2]
        startDatetime = line[3]
        startTime = int(line[4])
        gate = line[5]
        duration = int(line[6])
        endTime = int(line[7])
        endDatetime = line[8]
        
        if (not (currentTime <= startTime)):
            print currentTime, startTime
        assert currentTime <= startTime
        currentTime = startTime
        
        hangouts[gate].append([carId, startTime, endTime,carType,duration])
    
    
    #print "Full Camp List:"
    #for line in hangouts["C1"]: print line
    
    #generate arrivals and departures for each camp
    arrivals = {}
    departures = {} 
    for c in campNames:
        arrivals[c] = []
        departures[c] = []
        for carEntry in hangouts[c]:
            arrivals[c].append([carEntry[1],carEntry[0],carEntry[3],carEntry[4]])
            departures[c].append([carEntry[2],carEntry[0],carEntry[3],carEntry[4]])
            
    #sort departures
    for c in campNames:
        departures[c].sort(key=lambda x: x[0])
    
    #print "Arrivals:"
    #for t in arrivals["C6"]: print t
    #print "Departures:"
    #for t in departures["C6"]: print t 
    
    #initialize time series for each camp
    populationTimeSeries = {}
    population = {}
    for c in campNames:
        populationTimeSeries[c] = []
        population[c] = 0
        
    for c in campNames:
        currArrivals = arrivals[c]
        currDepartures = departures[c]
        currAind = 0
        currDind = 0   
            
        while True:
            time = car = carType = duration = None
                     
            atEndOfArrive = (currAind >= len(currArrivals) - 1)
            atEndOfDepart = (currDind >= len(currDepartures) - 1)
            
            #check not at the end of either list
            #if (c=="C1"): print currAind, currDind
            if not atEndOfArrive and not atEndOfDepart:
                #if (c == "C1"): 
                    #print currArrivals[currAind][0], " >? ", currDepartures[currDind][0]
                    #print int(currArrivals[currAind][0]) - int(currDepartures[currDind][0])
                if currArrivals[currAind][0] < currDepartures[currDind][0]:
                    time = currArrivals[currAind][0]
                    car = currArrivals[currAind][1]
                    carType = currArrivals[currAind][2]
                    duration = currArrivals[currAind][3]
                    
                    currAind += 1
                    population[c] += 1
                    
                    #if (c=="C6"): print [time,c,car,population[c]], "+"
                else:
                    time = currDepartures[currDind][0]
                    car = currDepartures[currDind][1]
                    carType = currArrivals[currDind][2]
                    duration = currArrivals[currDind][3]
                    
                    
                    currDind += 1
                    population[c] -= 1
                    
                    #if (c=="C6"): print [time,c,car,population[c]], "-"
            elif (atEndOfArrive):
                time = currDepartures[currDind][0]
                car = currDepartures[currDind][1]
                carType = currArrivals[currDind][2]
                duration = currArrivals[currDind][3]
                
                currDind += 1
                population[c] -= 1
                
                #if (c=="C6"): print [time,c,car,population[c]], "-*"
            elif (atEndOfDepart):
                time = currArrivals[currAind][0]
                car = currArrivals[currAind][1]
                carType = currArrivals[currAind][2]
                duration = currArrivals[currAind][3]
                
                currAind += 1
                population[c] += 1
                
                #if (c=="C6"): print [time,c,car,population[c]], "+*"
            #else:
                #if (c=="C6"): print [time,c,car,population[c]], "?"
            populationTimeSeries[c].append([time,c,car,population[c],carType,duration])
            
            if atEndOfArrive and atEndOfDepart:
                break
        
    return populationTimeSeries