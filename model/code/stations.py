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

input1 = "../model_data/vector_data/stationsV.shp"
table1 = "../model_data/meteo_data/1V.csv"
out1 = "../model_data/vector_data/meteo/meteoV.shp"

input2 = "../model_data/vector_data/stationsC.shp"
table2 = "../model_data/meteo_data/1C.csv"
out2 = "../model_data/vector_data/meteo/meteoC.shp"

out = "../model_data/vector_data/meteo/meteo.shp"

processing.runalg('qgis:joinattributestable', input1,table1,'Estación','Estación',out1)
processing.runalg('qgis:joinattributestable', input2,table2,'Estación','Estación',out2)

processing.runalg("qgis:mergevectorlayers",[out1,out2] , out)

out3 = "../model_data/raster_data/IDW/meteo.tif"

layer=QgsVectorLayer(out,"l","ogr")
QgsMapLayerRegistry.instance().addMapLayers([layer])

extent = layer.extent()
xmin = extent.xMinimum()
xmax = extent.xMaximum()
ymin = extent.yMinimum()
ymax = extent.yMaximum()

processing.runalg('saga:inversedistanceweighted', out,'temp media',1,2.0,False,1.0,1,100.0,0,-1.0,10.0,0,0,10.0,"%f,%f,%f,%f" %(xmin, xmax, ymin, ymax),100.0,0,0,None,3,out3)

out4 = "../model_data/raster_data/reclass/temperature.tif"
rules = "../model_data/rules/temperature.txt"

processing.runalg("grass7:r.reclass", out3,rules, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, out4)

QgsApplication.exitQgis() 
