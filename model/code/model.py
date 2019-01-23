# coding=utf-8

#   Import modules 
import sys 
from qgis.core import * 
from qgis.gui import * 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from qgis.utils import * 

from os.path import expanduser
#    Configure QGIS directories and start the app 
#    Not to be used in QGIS python editor 
app = QgsApplication([], True) 
QgsApplication.setPrefixPath("/usr", True) 
QgsApplication.initQgis() 
sys.path.append("/usr/share/qgis/python/plugins")
import processing 
from processing.core.Processing import Processing 
from processing.tools import * 
from qgis.analysis import *

import sys,os

Processing.initialize() 

input11 = "../model_data/raster_data/reclass/electric_lines.tif"
input21 = "../model_data/raster_data/reclass/cities.tif"
input31 = "../model_data/raster_data/reclass/roads.tif"
input41 = "../model_data/raster_data/reclass/NDVI.tif"
input51 = "../model_data/raster_data/reclass/temperature_8.tif"
input61 = "../model_data/raster_data/reclass/precipitations_8.tif"
input71 = "../model_data/raster_data/reclass/ilumination.tif"

input1 = QgsRasterLayer(input11,'input1')
input2 = QgsRasterLayer(input21,'input2')
input3 = QgsRasterLayer(input31,'input3')
input4 = QgsRasterLayer(input41,'input4')
input5 = QgsRasterLayer(input51,'input5')
input6 = QgsRasterLayer(input61,'input6')
input7 = QgsRasterLayer(input71,'input7')

entries = []

raster1 = QgsRasterCalculatorEntry()
raster1.ref="input1@1"
raster1.raster = input1
raster1.bandNumber = 1
entries.append(raster1)

raster2 = QgsRasterCalculatorEntry()
raster2.ref="input2@1"
raster2.raster = input2
raster2.bandNumber = 1
entries.append(raster2)

raster3 = QgsRasterCalculatorEntry()
raster3.ref="input3@1"
raster3.raster = input3
raster3.bandNumber = 1
entries.append(raster3)
 
raster4 = QgsRasterCalculatorEntry()
raster4.ref="input4@1"
raster4.raster = input4
raster4.bandNumber = 1
entries.append(raster4)

raster5 = QgsRasterCalculatorEntry()
raster5.ref="input5@1"
raster5.raster = input5
raster5.bandNumber = 1
entries.append(raster5)
 
raster6 = QgsRasterCalculatorEntry()
raster6.ref="input6@1"
raster6.raster = input6
raster6.bandNumber = 1
entries.append(raster6)

raster7 = QgsRasterCalculatorEntry()
raster7.ref="input7@1"
raster7.raster = input7
raster7.bandNumber = 1
entries.append(raster7)

output1 = "../results/ignition_risk.tif"

print "todo cargado"

calc = QgsRasterCalculator('(4*((input1@1 + input2@1 + input3@1)/3))+(3*((input4@1 + input5@1 + input6@1)/3))+(input7@1)', output1, "GTiff", input1.extent(), input1.width(), input1.height(), entries)

calc.processCalculation()

print "calculado1"

input81 = "../model_data/raster_data/reclass/siose.tif"
input91 = "../model_data/raster_data/reclass/slope.tif"
input101 = "../model_data/raster_data/reclass/wind_8.tif"
input111 = "../model_data/raster_data/reclass/orientation.tif"
#input121 = "../model_data/raster_data/reclass/rivers.tif"
#input131 = "../model_data/raster_data/reclass/firewalls.tif"
input141 = "../model_data/raster_data/reclass/water_points.tif"
#input151 = "../model_data/raster_data/reclass/water.tif"
input161 = "../model_data/raster_data/reclass/humidity_8.tif"

input8 = QgsRasterLayer(input81,'input8')
input9 = QgsRasterLayer(input91,'input9')
input10 = QgsRasterLayer(input101,'input10')
input11 = QgsRasterLayer(input111,'input11')
#input12 = QgsRasterLayer(input121,'input12')
#input13 = QgsRasterLayer(input131,'input13')
input14 = QgsRasterLayer(input141,'input14')
#input15 = QgsRasterLayer(input151,'input15')
input16 = QgsRasterLayer(input161,'input16')

entries2 = []

raster8 = QgsRasterCalculatorEntry()
raster8.ref="input8@1"
raster8.raster = input8
raster8.bandNumber = 1
entries2.append(raster8)

raster9 = QgsRasterCalculatorEntry()
raster9.ref="input9@1"
raster9.raster = input9
raster9.bandNumber = 1
entries2.append(raster9)

raster10 = QgsRasterCalculatorEntry()
raster10.ref="input10@1"
raster10.raster = input10
raster10.bandNumber = 1
entries2.append(raster10)

raster11 = QgsRasterCalculatorEntry()
raster11.ref="input11@1"
raster11.raster = input11
raster11.bandNumber = 1
entries2.append(raster11)

#raster12 = QgsRasterCalculatorEntry()
#raster12.ref="input12@1"
#raster12.raster = input12
#raster12.bandNumber = 1
#entries2.append(raster12)

#raster13 = QgsRasterCalculatorEntry()
#raster13.ref="input13@1"
#raster13.raster = input13
#raster13.bandNumber = 1
#entries2.append(raster13)

raster14 = QgsRasterCalculatorEntry()
raster14.ref="input14@1"
raster14.raster = input14
raster14.bandNumber = 1
entries2.append(raster14)

#raster15 = QgsRasterCalculatorEntry()
#raster15.ref="input15@1"
#raster15.raster = input15
#raster15.bandNumber = 1
#entries2.append(raster15)

raster16 = QgsRasterCalculatorEntry()
raster16.ref="input16@1"
raster16.raster = input16
raster16.bandNumber = 1
entries2.append(raster16)

#output2 = "../results/propagation_risk.tif"

#calc2 = QgsRasterCalculator('(5*(input8@1)) + (4*((input9@1+input10@1)/2)) + (3*(input11@1)) - ((input3@1+input12@1+input13@1)+((0.6*input14@1)+(0.4*input15@1))) - (input16@1)', output2, "GTiff", input1.extent(), input1.width(), input1.height(), entries)

#calc2.processCalculation()

QgsApplication.exitQgis() 
