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

input1 = "../model_data/raster_data/reclass/siose.tif"
input2 = "../model_data/raster_data/reclass/slope.tif"
input3 = "../model_data/raster_data/reclass/wind_8.tif"
input4 = "../model_data/raster_data/reclass/orientation.tif"

output = "../model_data/results/propagation1.tif"

processing.runalg('gdalogr:rastercalculator', input1,'1',input2,'1',input3,'1',input4,'1',None,'1',None,'1','5*A+4*((B+C)/2)+3*D',None,5,None,output)

QgsApplication.exitQgis() 
