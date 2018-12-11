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

QgsApplication.exitQgis() 
