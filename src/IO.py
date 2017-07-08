# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 19:48:10 2017

@author: Hume Dickie
"""

from config import imgDirectory, outputDirectory, dataDirectory
from config import mapName, rawDataName

from PIL import Image, ImageEnhance, ImageDraw, ImageFont
import random, os, csv
from ParkUtils import mapAbbrev, gateCoords

#processed data
from Transformations import rowsToIndiRecords, indiRecordsToCampRecords, sortedCampRecsToGroupHangouts


#Draw last label
def plotPath(visRec):
    #color scale end points
    c0 = (0,255,0,0)    #first color
    c1 = (255,0,0,0)    #second color
    
    os.chdir(imgDirectory)
    
    try:
        parkmap = Image.open(mapName)
    except:
        print "Unable to load image"
    
    #fade the map to make the paths easier to see
    contrast = ImageEnhance.Contrast(parkmap)
    faded = contrast.enhance(0.15)
    imgdraw = ImageDraw.Draw(faded)
    
    #draw lines
    for i in range(0,len(visRec.path)-1):
        
        n0 = mapAbbrev[visRec.path[i]]
        n1 = mapAbbrev[visRec.path[i+1]]
        
        iR = int((c1[0] - c0[0])*(float(i)/(len(visRec.path)-1)))
        iG = int((c1[1] - c0[1])*(float(i)/(len(visRec.path)-1)))
        iB = int((c1[2] - c0[2])*(float(i)/(len(visRec.path)-1)))
        ia = int((c1[3] - c0[3])*(float(i)/(len(visRec.path)-1)))
        
        if (iR < 0) : iR = 255 + iR
        if (iG < 0) : iG = 255 + iG
        if (iB < 0) : iB = 255 + iB
        if (ia < 0) : ia = 255 + ia
        
        #jitter
        j1 = random.randint(-25,25)
        j2 = random.randint(-25,25)
        
        x0 = gateCoords[n0][0] + j1  
        y0 = gateCoords[n0][1] + j2
        x1 = gateCoords[n1][0] + j1
        y1 = gateCoords[n1][1] + j2
        
        imgdraw.line((x0,y0,x1,y1),
                      fill=(iR,iG,iB,ia), 
                      width = 1)
                      
        fontsize = 20
                      
        font = ImageFont.truetype("arial.ttf", fontsize)                      
                      
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
    os.chdir(outputDirectory)     
    
    asDF = open("individual-records.txt",'w')
    asDF.write("car.id;car.type;enterTime;length;totalTime;N1;dt1;N2;dt2;N3;dt3;N4;dt4;N5;dt5;N6;dt6;N7;dt7;N8;dt8;N9;dt9;N10;dt10;N11;dt11;N12;dt12;N13;dt13;N14;dt14;N15;dt15;N16;dt16;N17;dt17;N18;dt18;N19;dt19;N20;dt20;N21;dt21;N22;dt22;N23;dt23;N24;dt24;N25;dt25;N26;dt26;N27;dt27;N28;dt28;N29;dt29;N30;dt30;N31;dt31;N32;dt32;N33;dt33;N34;dt34;N35;dt35;N36;dt36;N37;dt37;N38;dt38;N39;dt39;N40;dt40;N41;dt41;N42;dt42;N43;dt43;N44;dt44;N45;dt45;N46;dt46;N47;dt47;N48;dt48;N49;dt49;N50;dt50;N51;dt51;N52;dt52;N53;dt53;N54;dt54;N55;dt55;N56;dt56;N57;dt57;N58;dt58;N59;dt59;N60;dt60;N61;dt61;N62;dt62;N63;dt63;N64;dt64;N65;dt65;N66;dt66;N67;dt67;N68;dt68;N69;dt69;N70\n")
    for key in records:
        for d in records[key]:
            asDF.write(d.asDataFrameEntry())
    asDF.close()
    os.chdir(prevDir)
    
def writeCampsiteRecords(campRecs):
    prevDir = os.getcwd()
    os.chdir(outputDirectory)
    
    campsiteRecords = open("campsite-records.txt",'w')
    campsiteRecords.write("car.id,car.type,startDatetime,startTimestamp,gate.name,duration,endTimestamp,endDatetime\n")
    for line in campRecs:
        campsiteRecords.write(line)
    campsiteRecords.close()
    os.chdir(prevDir)
    
def getRawData():
    prevDir = os.getcwd()
    os.chdir(dataDirectory)
    
    lines = []
    with open(rawDataName) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            lines.append(row)    
    
    os.chdir(prevDir)
    return lines
    
#recomputes. Does not read from output file
def getIndividualRecords():
    prevDir = os.getcwd()
    os.chdir(dataDirectory)
    
    records = rowsToIndiRecords(rawDataName)
    os.chdir(prevDir)
    
    return records

#Reads from IndividualRecords output file. Recompute campRecords.
def getCampsiteRecords():
    prevDir = os.getcwd()
    os.chdir(outputDirectory)
    
    indiRecordsLines = []
    try:
        with open("individual-records.txt",'r') as csvfile:
            reader = csv.reader(csvfile,delimiter=";")
            for row in reader:
                indiRecordsLines.append(row)
    except:
        print "Failed to open campsite records. Does that file exist?"
        
    
    
    records = indiRecordsToCampRecords(indiRecordsLines)
    os.chdir(prevDir)
    
    return records
    
#Reads from sorted campsite records
def getGroupHangouts():
    prevDir = os.getcwd()
    os.chdir(outputDirectory)
    
    sortedLines = []
    try:
        with open("campsite-records-sorted.csv",'r') as csvfile:
            reader = csv.reader(csvfile,delimiter=",")
            for row in reader:
                sortedLines.append(row)
    except:
        print "Failed to open sorted campsite records. Does that file exist?"
    
    os.chdir(prevDir)    
    
    hangouts = sortedCampRecsToGroupHangouts(sortedLines)
    
    return hangouts
      
def writeGroupHangouts(hangouts):
    prevDir = os.getcwd()
    os.chdir(outputDirectory)

    groups = open("campsite-population-time-series.txt",'w')
    groups.write("time,gate,car.id,population\n")
    for camp in hangouts:
        for line in hangouts[camp]:
            temp = str(line[0]) + "," + str(line[1]) + "," + str(line[2]) + "," + str(line[3]) + "\n"
            groups.write(temp)
    groups.close()
    
    os.chdir(prevDir)
#TODO
def plotPathsAsHeat(listOfPaths):
    print 5
    
#TODO
def plotPaths(listOfPaths):
    print 5