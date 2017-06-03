# -*- coding: utf-8 -*-
"""
Created on Mon May 29 11:20:35 2017

@author: Hume Dickie
"""

import csv
from datetime import datetime as dt

from VisitRecord import VisitRecord
from ParkUtils import isEntranceOrBase

def rowsToRecords(fileName):
    
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
            #carType = line[2]
            gate = line[3]
            
            is_entrance = isEntranceOrBase(gate)
            if carId not in records:
                records[carId] = [VisitRecord(timestamp,gate,carId,not is_entrance)]
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
    
    return records
    
