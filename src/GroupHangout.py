# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 20:40:16 2017

@author: Hume Dickie
"""

#GroupHangout.py
class GroupHangout:
    def __init__(self,carId,startTime,endTime,gate):
        
        self.startTime = startTime
        self.endTime = endTime
        self.gate = gate
        
        self.maxSize = 1
        self.size = 1
        
        newCar = GroupHangout.Car(carId,startTime,endTime)        
        self.cars = [newCar]
        
    def addCar(self,carId,arriveTime,exitTime):
        if carId in self.camperIDs:
            print "WARNING"
            print carId, " was already at campsite ", self.gate, " when it (allegedly!) arrived."
            
        self.cars.append(GroupHangout.Car(carId,arriveTime,exitTime))
        self.size += 1
        
        if (len(self.camperIDs) > self.maxSize):
            self.maxSize = len(self.cars)
            
        if carId not in self.camperIDs:
            newCar = GroupHangout.Car(carId,arriveTime,exitTime) 
            self.cars.append(newCar)
            
    def close():
        print 5
        #TODO
            
    def containsCar(self,carId):
        return carId in self.camperIDs
    
    def getDuration(self):
        if self.endTime is None:
            #the latest timeStamp in the data set
            assert (1464563122 - int(self.startTime) >= 0)
            return 1464563122 - int(self.startTime)
        else:
            return int(self.endTime) - int(self.startTime)
    
    def __repr__(self):
        running = "Group Hangout: "
        running += str(self.startTime) + "; "
        running += self.gate +"; "
        for member in self.groupMembers:
            running += member.carId +", "
        running = running[0:len(running)-2] + "; " #replace last comma w ;
        running += str(self.getDuration())
        running = running[0:len(running)-1] #remove last comma
        return running
        
    class Car:
        def __init__(self,carId,arriveTime,exitTime):
            self.carId = carId
            self.arriveTime = arriveTime
            self.exitTime = exitTime
            
        def __repr__(self):
            return self.carId