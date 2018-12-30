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

import sys,os

Processing.initialize() 

vector = "../model_data/vector_data/roads.shp"
layer=QgsVectorLayer(vector,"l","ogr")
QgsMapLayerRegistry.instance().addMapLayers([layer])

rules = "../model_data/rules/slope.txt"

extent = layer.extent()
xmin = extent.xMinimum()
xmax = extent.xMaximum()
ymin = extent.yMinimum()
ymax = extent.yMaximum()

input = "../model_data/DTM/mdt25.tif"
output1 = "../model_data/DTM/slope/slope.tif"
#processing.runalg('gdalogr:slope', input, 1.0, False, False, True, 1.0, output1)

output2 = "../model_data/raster_data/reclass/slope.tif"
#processing.runalg("grass7:r.reclass", output1,rules, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, output2)

QgsApplication.exitQgis() 
