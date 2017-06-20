# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 20:40:16 2017

@author: Hume Dickie
"""

#GroupHangout.py
class GroupHangout:
    def __init__(self,carId,startTimestamp,gate):
        
        self.firstCar = carId
        self.startTime = startTimestamp
        self.endTime = None
        self.gate = gate
        
        self.camperIDs = [carId]
        self.lastCar = None
        self.maxSize = 1
        self.size = 1
        
        newCar = GroupHangout.GroupMember(carId,startTimestamp)        
        self.groupMembers = [newCar]
        
    def addCamper(self,carId,arriveTime):
        if carId in self.camperIDs:
            print "WARNING"
            print carId, " was already at campsite ", self.gate, " when it arrived."
            
        self.camperIDs.append(carId)
        self.groupMembers.append(GroupHangout.GroupMember(carId,arriveTime))
        self.size += 1
        
        if (len(self.camperIDs) > self.maxSize):
            self.maxSize = len(self.camperIDs)
            
        if carId not in self.camperIDs:
            newCar = GroupHangout.GroupMember(carId,arriveTime) 
            self.groupMembers.append(newCar)
        
    def removeCamper(self,carId,departTime):
        if carId not in self.camperIDs:
            print "WARNING"
            print carId, " was not at campsite ", self.gate, " when it left."
            
        self.camperIDs.remove(carId)
        self.size -= 1
        
        if (len(self.camperIDs) == 0):
            self.lastCar = carId
            self.endTime = departTime
            
    def containsCamper(self,carId):
        return carId in self.camperIDs
            
    def getGroupMembers(self):
        return self.groupMembers
        
    def maxSize(self):
        return self.maxSize
        
    def getSize(self):
        return self.size
    
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
        
    class GroupMember:
        def __init__(self,carId,arriveTime):
            self.carId = carId
            self.arriveTime = arriveTime
            
        def __repr__(self):
            return self.carId