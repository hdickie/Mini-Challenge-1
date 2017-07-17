# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 18:19:23 2017

@author: Hume Dickie
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 02 18:09:55 2017

@author: Hume Dickie
"""

#parkStructs.py

import re

ignoreList = ["20155705025759-63", #the weird car

              "20162904122951-717", #repeat camper: green
              "20153712013720-181", #repeat camper: blue
              "20154112014114-381", #repeat camper: orange
              "20154519024544-322", #repeat camper: red
              
              "20162027042012-940", #at least 3 visits, at most 1 camp
              
              "20153427103455-30", #two visits, at most 1 camp
              "20150322080300-861",
              "20160623090611-424",
              "20161008061012-639",
              "20150204100226-134",
              "20154501084537-684"
              ]

mapAbbrev = {"entrance0" : "E0",
             "entrance1" : "E1",
             "entrance2" : "E2",
             "entrance3" : "E3",
             "entrance4" : "E4",
             "camping0" : "C0",
             "camping1" : "C1",
             "camping2" : "C2",
             "camping3" : "C3",
             "camping4" : "C4",
             "camping5" : "C5",
             "camping6" : "C6",
             "camping7" : "C7",
             "camping8" : "C8",
             "general-gate0" : "GG0",
             "general-gate1" : "GG1",
             "general-gate2" : "GG2",
             "general-gate3" : "GG3",
             "general-gate4" : "GG4",
             "general-gate5" : "GG5",
             "general-gate6" : "GG6",
             "general-gate7" : "GG7",
             "general-gate8" : "GG8",
             "ranger-stop0" : "R0",
             "ranger-stop1" : "R1",
             "ranger-stop2" : "R2",
             "ranger-stop3" : "R3",
             "ranger-stop4" : "R4",
             "ranger-stop5" : "R5",
             "ranger-stop6" : "R6",
             "ranger-stop7" : "R7",
             "gate0" : "G0",
             "gate1" : "G1",
             "gate2" : "G2",
             "gate3" : "G3",
             "gate4" : "G4",
             "gate5" : "G5",
             "gate6" : "G6",
             "gate7" : "G7",
             "gate8" : "G8",
             "ranger-base" : "B"
             }
             
nodeIndex = {"E0" : 0,
             "E1" : 1,
             "E2" : 2,
             "E3" : 3,
             "E4" : 4,
             "C0" : 5,
             "C1" : 6,
             "C2" : 7,
             "C3" : 8,
             "C4" : 0,
             "C5" : 10,
             "C6" : 11,
             "C7" : 12,
             "C8" : 13,
             "GG0" : 14,
             "GG1" : 15,
             "GG2" : 16,
             "GG3" : 17,
             "GG4" : 18,
             "GG5" : 19,
             "GG6" : 20,
             "GG7" : 21,
             "GG8" : 22,
             "R0" : 23,
             "R1" : 24,
             "R2" : 25,
             "R3" : 26,
             "R4" : 27,
             "R5" : 30,
             "R6" : 31,
             "R7" : 32,
             "G0" : 33,
             "G1" : 34,
             "G2" : 35,
             "G3" : 36,
             "G4" : 37,
             "G5" : 38,
             "G6" : 39,
             "G7" : 40,
             "G8" : 41,
              "B" : 42
             }

gateCoords = {"E0" : (310,69),
              "E1" : (90,331),
              "E2" : (898,430),
              "E3" : (566,818),
              "E4" : (688,903),
              "C0" : (259,205),
              "C1" : (634,248),
              "C2" : (220,318),
              "C3" : (225,335),
              "C4" : (240,436),
              "C5" : (101,595),
              "C6" : (736,869),
              "C7" : (889,710),
              "C8" : (898,240),
              "GG0" : (542,50),
              "GG1" : (319, 129),
              "GG2" : (511,161),
              "GG3" : (913,273),
              "GG4" : (344,482),
              "GG5" : (609,546),
              "GG6" : (668,673),
              "GG7" : (322,704),
              "R0" : (440,84),
              "R1" : (98,121),
              "R2" : (395,174),
              "R3" : (727,224),
              "R4" : (93,467),
              "R5" : (740,581),
              "R6" : (606, 722),
              "R7" : (494, 744),
              "G0" : (312,167),
              "G1" : (288,220),
              "G2" : (122,270),
              "G3" : (732, 297),
              "G4" : (805,559),
              "G5" : (644,716),
              "G6" : (571, 740),
              "G7" : (477,785),
              "G8" : (678, 886),
              "B" : (628,856)
              }
              
def isEntranceOrBase(gate):
    t = re.search("entrance[0-4]",gate)
    is_e = hasattr(t,"group")
    is_b = (gate == "ranger-base")
    return is_e or is_b
    
def isCampsite(gate):
    return re.search("camping[0-8]",gate)
    