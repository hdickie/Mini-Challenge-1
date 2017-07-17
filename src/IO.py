# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 19:48:10 2017

@author: Hume Dickie
"""

from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import random, os, csv,time, datetime, sys
import Transformations, ParkUtils, config, PopulationMonitor


#Draw last label
def plotPath(visRec):
    #color scale end points
    c0 = (0,255,0,0)    #first color
    c1 = (255,0,0,0)    #second color
    
    os.chdir(config.imgDirectory)
    
    try:
        parkmap = Image.open(ParkUtils.mapName)
    except:
        print "Unable to load image"
    
    #fade the map to make the paths easier to see
    contrast = ImageEnhance.Contrast(parkmap)
    faded = contrast.enhance(0.5)
    imgdraw = ImageDraw.Draw(faded)
    
    #draw lines
    for i in range(0,len(visRec.path)-1):
        
        n0 = ParkUtils.mapAbbrev[visRec.path[i]]
        n1 = ParkUtils.mapAbbrev[visRec.path[i+1]]
        
        iR = int((c1[0] - c0[0])*(float(i+1)/(len(visRec.path))))
        iG = int((c1[1] - c0[1])*(float(i+1)/(len(visRec.path))))
        iB = int((c1[2] - c0[2])*(float(i+1)/(len(visRec.path))))
        ia = int((c1[3] - c0[3])*(float(i+1)/(len(visRec.path))))
        
        if (iR < 0) : iR = 255 + iR
        if (iG < 0) : iG = 255 + iG
        if (iB < 0) : iB = 255 + iB
        if (ia < 0) : ia = 255 + ia
        
        #jitter
        j1 = random.randint(-25,25)
        j2 = random.randint(-25,25)
        
        x0 = ParkUtils.gateCoords[n0][0] + j1  
        y0 = ParkUtils.gateCoords[n0][1] + j2
        x1 = ParkUtils.gateCoords[n1][0] + j1
        y1 = ParkUtils.gateCoords[n1][1] + j2
        
        imgdraw.line((x0,y0,x1,y1),
                      fill=(iR,iG,iB,ia), 
                      width = 1)
                      
        fontsize = 20
                      
        font = ImageFont.truetype("arial.ttf", fontsize)                      
                      
        imgdraw.text((x0,y0),str(i),font = font)
        
        #draw last label
        if (i == len(visRec.path)-2):
            imgdraw.text((x1,y1),str(i),font = font)
    
    return faded

#Dont think we need this anymore
#def writeVisits(records):
#    prevDir = os.getcwd()
#    os.chdir(outputDirectory)
#    
#    visits = open("visits.txt",'w')
#    for key in records:
#        for v in records[key]:
#            visits.write(v.toString())
#    visits.close()
#    os.chdir(prevDir)
    
#def writePaths(records):
#    prevDir = os.getcwd()
#    os.chdir(outputDirectory)    
#    
#    paths = open("paths.txt",'w')
#    for key in records:
#        for p in records[key]:
#            paths.write(p.pathString())
#    paths.close()
#    os.chdir(prevDir)

def writeIndividualRecords(records):
    prevDir = os.getcwd()
    os.chdir(config.outputDirectory)     
    
    asDF = open("individual-records-2.txt",'w')
    asDF.write("car.id;car.type;enterTime;length;totalTime;N1;dt1;N2;dt2;N3;dt3;N4;dt4;N5;dt5;N6;dt6;N7;dt7;N8;dt8;N9;dt9;N10;dt10;N11;dt11;N12;dt12;N13;dt13;N14;dt14;N15;dt15;N16;dt16;N17;dt17;N18;dt18;N19;dt19;N20;dt20;N21;dt21;N22;dt22;N23;dt23;N24;dt24;N25;dt25;N26;dt26;N27;dt27;N28;dt28;N29;dt29;N30;dt30;N31;dt31;N32;dt32;N33;dt33;N34;dt34;N35;dt35;N36;dt36;N37;dt37;N38;dt38;N39;dt39;N40;dt40;N41;dt41;N42;dt42;N43;dt43;N44;dt44;N45;dt45;N46;dt46;N47;dt47;N48;dt48;N49;dt49;N50;dt50;N51;dt51;N52;dt52;N53;dt53;N54;dt54;N55;dt55;N56;dt56;N57;dt57;N58;dt58;N59;dt59;N60;dt60;N61;dt61;N62;dt62;N63;dt63;N64;dt64;N65;dt65;N66;dt66;N67;dt67;N68;dt68;N69;dt69;N70\n")
    for key in records:
        for d in records[key]:
            asDF.write(d.asDataFrameEntry())
    asDF.close()
    os.chdir(prevDir)
    
def writeCampsiteRecords(campRecs):
    prevDir = os.getcwd()
    os.chdir(config.outputDirectory)
    
    campsiteRecords = open("campsite-records.txt",'w')
    campsiteRecords.write("car.id,car.type,startDatetime,startTimestamp,gate.name,duration,endTimestamp,endDatetime\n")
    for line in campRecs:
        campsiteRecords.write(line)
    campsiteRecords.close()
    os.chdir(prevDir)
    
def getRawData():
    prevDir = os.getcwd()
    os.chdir(config.dataDirectory)
    
    lines = []
    with open(config.rawDataName) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lines.append(row)    
    
    os.chdir(prevDir)
    return lines
    
#recomputes. Does not read from output file
def getIndividualRecords():
    prevDir = os.getcwd()
    os.chdir(config.dataDirectory)
    
    records = Transformations.rowsToIndiRecords(config.rawDataName)
    os.chdir(prevDir)
    
    return records

#Reads from IndividualRecords output file. Recompute campRecords.
def getCampsiteRecords():
    prevDir = os.getcwd()
    os.chdir(config.outputDirectory)
    
    indiRecordsLines = []
    try:
        with open("individual-records.txt",'r') as csvfile:
            reader = csv.reader(csvfile,delimiter=";")
            for row in reader:
                indiRecordsLines.append(row)
    except:
        print "Failed to open campsite records. Does that file exist?"
        
    
    
    records = Transformations.indiRecordsToCampRecords(indiRecordsLines)
    os.chdir(prevDir)
    
    return records
    
#Reads from sorted campsite records
def getGroupHangouts():
    prevDir = os.getcwd()
    os.chdir(config.outputDirectory)
    
    sortedLines = []
    try:
        with open("campsite-records-sorted.csv",'r') as csvfile:
            reader = csv.reader(csvfile,delimiter=",")
            for row in reader:
                sortedLines.append(row)
    except:
        print "Failed to open sorted campsite records. Does that file exist?"
    
    os.chdir(prevDir)    
    
    hangouts = Transformations.sortedCampRecsToGroupHangouts(sortedLines)
    
    return hangouts
      
def writeGroupHangouts(hangouts):
    prevDir = os.getcwd()
    os.chdir(config.outputDirectory)

    groups = open("campsite-population-time-series.txt",'w')
    groups.write("time,gate,car.id,population,carType,duration\n")
    for camp in hangouts:
        for line in hangouts[camp]:
            temp = str(line[0]) + "," + str(line[1]) + "," + str(line[2]) + "," + str(line[3]) + "," + str(line[4]) + "," + str(line[5]) + "\n"
            groups.write(temp)
    groups.close()
    
    os.chdir(prevDir)
    
def getPopTimeSeries():
    prevDir = os.getcwd()
    os.chdir(config.outputDirectory)
    
    lines = []
    try:
        with open("C7-in-out.csv",'r') as csvfile:
            reader = csv.reader(csvfile,delimiter=",")
            for row in reader:
                lines.append(row)
    except:
        print "Failed to in-out. Does that file exist?"
    
    os.chdir(prevDir)    
    
    inOut = Transformations.inOutToPopTimeSeries(lines)
    
    return inOut
    
def writePopTimeSeries(inOutLines):
    prevDir = os.getcwd()
    os.chdir(config.outputDirectory)

    groups = open("pop-time-series.csv",'w')
    groups.write("time,gate,car.id,population,carType,duration\n")
    for line in inOutLines:
        temp = str(line[0]) + "," + str(line[1]) + "," + str(line[2]) + "," + str(line[3]) + "," + str(line[4]) + "," + str(line[5]) + "\n"
        groups.write(temp)
    groups.close()
    
    os.chdir(prevDir)

def getCampListForEachCar():
    campRecords = getCampsiteRecords()
    campLists = {}

    for line in campRecords:
        line = line.split(",")
        line[7] = line[7][0:(len(line[7])-1)] #trim newline
        
        carID = line[0]
        enterDatetime = line[2]
        enterTimestamp = line[3]
        gate = line[4]
        duration = line[5]
        endTimestamp = line[6]
        endDatetime = line[7]
    
        newEntry = [enterDatetime,enterTimestamp,gate,duration,endTimestamp,endDatetime]    
    
        if carID not in campLists:
            campLists[carID] = [newEntry]
        else:
            campLists[carID].append(newEntry)
            
    return campLists

def toIntTime(stringDatetime):
    return time.mktime(datetime.datetime.strptime(stringDatetime,"%Y-%m-%d %H:%M:%S").timetuple())
    
def visitedRangerStopOrBase(line):
    targetStops = set(["R0","R1","R2","R3","R4","R5","R6","R7","B"])
    observedStops = set(line)
    
    return not targetStops.isdisjoint(observedStops)

def getNumCampStays(line):
    justDTs = list(filter(lambda x: type(x) == int, line))

    return len(list(filter(lambda x: x > 60*60*12, justDTs)))
#ignorw those 5 return cars it will make a lot of shit easier
def getMasterSheet(verbose):
    alogrithmStartTime = datetime.datetime.now()
    olines = []
    
    if (verbose): print "getting camp lists"
    campLists = getCampListForEachCar()      
    if (verbose): print "getting individual records"
    indiLines = getIndividualRecords()
    if (verbose): print "initializing population monitor"
    monitor = PopulationMonitor.PopulationMonitor()
    if (verbose): 
        print "building sheet"
        total = len(indiLines)
        place = 0
        cycle = 187
        
    for car in indiLines:
        if (verbose):
            place +=1
            if (place % cycle == 0):
                print str((100*float(place)/float(total)))[0:5] + "%"
        
        if car in ParkUtils.ignoreList:
            continue
        
        line = indiLines[car][0].asDataFrameEntry().split(";")
        
        carID = line[0]
        carType = line[1]
        enterParkTime = line[2]
        
        counts = monitor.getCampCounts(toIntTime(enterParkTime))
        C0p = counts[0]
        C1p = counts[1]
        C2p = counts[2]
        C3p = counts[3]
        C4p = counts[4]
        C5p = counts[5]
        C6p = counts[6]
        C7p = counts[7]
        C8p = counts[8]
        
        classification = "None-Default"
        visitedRB = visitedRangerStopOrBase(line)
        numCampStays = getNumCampStays(line)
        
        if carID not in campLists:
            campArriveTime = campArriveTimestamp = camp = duration = endCampTime = endCampTimestamp = "N/A"
        else:
            curr = campLists[carID][0]
            
            campArriveTime = curr[0]
            campArriveTimestamp = curr[1]
            camp = curr[2]
            duration = curr[3]
            endCampTime = curr[4]
            endCampTimestamp = curr[5]
            
        oline = carID + "," + carType + "," + enterParkTime + ","
        oline += str(C0p) + "," + str(C1p) + "," + str(C2p) + "," + str(C3p) + "," + str(C4p) + "," + str(C5p) + "," + str(C6p) + "," + str(C7p) + "," + str(C8p) + ","
        oline += str(visitedRB)  + "," + str(numCampStays)  + ","
        oline += campArriveTime + "," + campArriveTimestamp + "," + camp + "," + duration + "," + endCampTime + "," + endCampTimestamp
        
        for i in range(3,len(line)):
            oline += "," + line[i]
            
        olines.append(oline)
        
    print "getMasterSheet took ", str(datetime.datetime.now() - alogrithmStartTime)
    return olines

def writeMasterSheet(verbose):
    prevDir = os.getcwd()
    os.chdir(config.outputDirectory)
    
    master = open("master-sheet.csv",'w')
    headers = "car.id,car.type,enterParkTime,C0p,C1p,C2p,C3p,C4p,C5p,C6p,C7p,C8p,visitedRB,numCampStays,campArriveTime,campArriveTimestamp,camp,duration,endCampTime,endCampTimestamp,pathLength,totalTime,N1,dt1,N2,dt2,N3,dt3,N4,dt4,N5,dt5,N6,dt6,N7,dt7,N8,dt8,N9,dt9,N10,dt10,N11,dt11,N12,dt12,N13,dt13,N14,dt14,N15,dt15,N16,dt16,N17,dt17,N18,dt18,N19,dt19,N20,dt20,N21,dt21,N22,dt22,N23,dt23,N24,dt24,N25,dt25,N26,dt26,N27,dt27,N28,dt28,N29,dt29,N30,dt30,N31,dt31,N32,dt32,N33,dt33,N34,dt34,N35,dt35,N36,dt36,N37,dt37,N38,dt38,N39,dt39,N40,dt40,N41,dt41,N42,dt42,N43,dt43,N44,dt44,N45,dt45,N46,dt46,N47,dt47,N48,dt48,N49,dt49,N50,dt50,N51,dt51,N52,dt52,N53,dt53,N54,dt54,N55,dt55,N56,dt56,N57,dt57,N58,dt58,N59,dt59,N60,dt60,N61,dt61,N62,dt62,N63,dt63,N64,dt64,N65,dt65,N66,dt66,N67,dt67,N68,dt68,N69,dt69,N70\n"
    
    mss = getMasterSheet(verbose)    
    
    master.write(headers)
    for line in mss:
        master.write(line)
        
    master.close()
    os.chdir(prevDir)
    
def classify(line):
    line = line.split(",")
    
    pathLength = int(line[20])
    carType = line[1]
    
    if (pathLength == 2 or pathLength == 3):
        return "Traffic"
        
    if (carType == "2P"):
        return "Ranger"
        
    if (ParkUtils.isEntranceOrBase(line[len(line)-1])):
        return "Camper - Never Left"
        
    #if "0" in line[22:len(line)]: return "dt 0"
    
    return "None"
    
def getMasterPlusClassification():
    prevDir = os.getcwd()
    os.chdir(config.outputDirectory)
    
    master = open("master-sheet.csv",'r')
    lines = []
    
    isFirstLine = True
    for line in master:
        if (isFirstLine):
            isFirstLine = False
            continue
        #line might be an array
        line = classify(line) + "," + line         
        lines.append(line)
        
    master.close()
    os.chdir(prevDir)
    return lines
    
def writeMasterPlusClassification():
    prevDir = os.getcwd()
    os.chdir(config.outputDirectory)
    
    master = open("master-sheet-plus-class.csv",'w')
    lines = getMasterPlusClassification()
    
    headers = "class,car.id,car.type,enterParkTime,C0p,C1p,C2p,C3p,C4p,C5p,C6p,C7p,C8p,visitedRB,numCampStays,campArriveTime,campArriveTimestamp,camp,duration,endCampTime,endCampTimestamp,pathLength,totalTime,N1,dt1,N2,dt2,N3,dt3,N4,dt4,N5,dt5,N6,dt6,N7,dt7,N8,dt8,N9,dt9,N10,dt10,N11,dt11,N12,dt12,N13,dt13,N14,dt14,N15,dt15,N16,dt16,N17,dt17,N18,dt18,N19,dt19,N20,dt20,N21,dt21,N22,dt22,N23,dt23,N24,dt24,N25,dt25,N26,dt26,N27,dt27,N28,dt28,N29,dt29,N30,dt30,N31,dt31,N32,dt32,N33,dt33,N34,dt34,N35,dt35,N36,dt36,N37,dt37,N38,dt38,N39,dt39,N40,dt40,N41,dt41,N42,dt42,N43,dt43,N44,dt44,N45,dt45,N46,dt46,N47,dt47,N48,dt48,N49,dt49,N50,dt50,N51,dt51,N52,dt52,N53,dt53,N54,dt54,N55,dt55,N56,dt56,N57,dt57,N58,dt58,N59,dt59,N60,dt60,N61,dt61,N62,dt62,N63,dt63,N64,dt64,N65,dt65,N66,dt66,N67,dt67,N68,dt68,N69,dt69,N70\n"
    master.write(headers)
    for line in lines:
        master.write(line)
    
    master.close()
    os.chdir(prevDir)
    
    return lines
    
    