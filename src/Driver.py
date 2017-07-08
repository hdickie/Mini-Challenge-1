# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 17:58:25 2017

@author: Hume Dickie
"""
from IO import getIndividualRecords, plotPath

records = getIndividualRecords()

plot = plotPath(records["20155201075209-669"][0])

plot.show()