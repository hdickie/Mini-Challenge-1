# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 17:58:25 2017

@author: Hume Dickie
"""

#Driver.py

from IO import writeIndividualRecords, writeCampsiteRecords
from IO import getIndividualRecords, getCampsiteRecords, getGroupHangouts

#records = getIndividualRecords()
#writeIndividualRecords(records)

campRecs = getCampsiteRecords()
writeCampsiteRecords(campRecs)

#sortedRecs = getGroupHangouts()
  
#weird car "20155705025759-63"
# a ranger "20153722123707-242"
#plot = plotPath(records["20155201075209-669"][0])

#plot.show()
#if this code isn't working then make sure config.py is right

#campRecs = pathsToCampRecords("abbrev-paths.txt")

#os.chdir(outputDirectory)
#recs = open("campRecords.txt",'w')
#recs.write("car.id;beginTimestamp;gate.name;duration\n")
#for rec in campRecs:
#    recs.write(rec)
#recs.close()