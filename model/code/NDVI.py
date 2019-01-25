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

def NDVI(input11, input21, season):

	input1 = QgsRasterLayer(input11,'input1')
	input2 = QgsRasterLayer(input21,'input2')

	output = "../model_data/raster_data/NDVI/NDVI_"+season+".tif"

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

	calc = QgsRasterCalculator('(input2@1 - input1@1)/(input2@1 + input1@1)', output, "GTiff", input1.extent(), input1.width(), input1.height(), entries)

	calc.processCalculation()
	print "calc"

	rules = "../model_data/rules/NDVI.txt"
	output2 = "../model_data/raster_data/reclass/NDVI_"+season+".tif"

	la = "../model_data/vector_data/rivers.shp"
	layer=QgsVectorLayer(la,"l","ogr")
	QgsMapLayerRegistry.instance().addMapLayers([layer])

	extent = layer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()

	processing.runalg("grass7:r.reclass", output,rules, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, output2)
	print "reclass"

input11 = "../model_data/Lansat_images/summer/summer_3.tif"
input21 = "../model_data/Lansat_images/summer/summer_4.tif"
season1 = "summer"

NDVI(input11, input21, season1)
print "NDVI 1"

input12 = "../model_data/Lansat_images/spring/spring_3.tif"
input22 = "../model_data/Lansat_images/spring/spring_4.tif"
season2 = "spring"

NDVI(input12, input22, season2)
print "NDVI 2"

input13 = "../model_data/Lansat_images/autumn/autumn_3.tif"
input23 = "../model_data/Lansat_images/autumn/autumn_4.tif"
season3 = "autumn"

NDVI(input13, input23, season3)
print "NDVI 3"

input14 = "../model_data/Lansat_images/winter/winter_3.tif"
input24 = "../model_data/Lansat_images/winter/winter_4.tif"
season4 = "winter"

NDVI(input14, input24, season4)
print "NDVI 4"

QgsApplication.exitQgis() 
