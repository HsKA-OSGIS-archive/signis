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

input11 = "../model_data/Lansat_images/summer/b3_ago02.tif"
input21 = "../model_data/Lansat_images/summer/b4_ago02.tif"
season = "summer"

NDVI(input11, input21, season)

QgsApplication.exitQgis() 
