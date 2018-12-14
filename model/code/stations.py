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
import pandas as pd

reload(sys)  
sys.setdefaultencoding('utf8')

Processing.initialize() 

def station_interpolation(input,month):

	layer=QgsVectorLayer(input,"l","ogr")
	QgsMapLayerRegistry.instance().addMapLayers([layer])

	extent = layer.extent()
	xmin = extent.xMinimum()
	xmax = extent.xMaximum()
	ymin = extent.yMinimum()
	ymax = extent.yMaximum()

	var = ["temperature","precipitations","humidity","wind"]
	fields = ["temp media","Precipitac","Humedad re","Velocidad"]
	
	for i in range(len(var)):

		name = var[i]
		field = fields[i]

		out1 = "../model_data/raster_data/IDW/"+name+"_"+str(month)+".tif"

		processing.runalg('saga:inversedistanceweighted', input,field,1,2.0,False,1.0,1,100.0,0,-1.0,10.0,0,0,10.0,"%f,%f,%f,%f" %(xmin, xmax, ymin, ymax),100.0,0,0,None,3,out1)

		rules = "../model_data/rules/"+name+".txt"
		out2 = "../model_data/raster_data/reclass/"+name+"_"+str(month)+".tif"

		processing.runalg("grass7:r.reclass", out1,rules, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, out2)

month = 8;
input = "../model_data/vector_data/meteo/meteo_"+str(month)+".shp"

station_interpolation(input,month)

QgsApplication.exitQgis() 
