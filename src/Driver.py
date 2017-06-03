# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 17:58:25 2017

@author: Hume Dickie
"""

#Driver.py

import os
from config import dataDirectory, rawDataName
from rowsToRecords import rowsToRecords
from Output import writeOutputFiles, plotPath

os.chdir(dataDirectory)
records = rowsToRecords(rawDataName) 

writeOutputFiles(records)
  
#weird car "20155705025759-63"
# a ranger "20153722123707-242"
plot = plotPath(records["20153722123707-242"][0])

plot.show()


#if this code isn't working then make sure congif.py is right