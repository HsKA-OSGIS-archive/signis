# coding=utf-8

#Initialisierung und Beenden von QGIS in Python: 
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

def stations_join(tableC, tableV, month):

	input1 = "../model_data/vector_data/stationsV.shp"
	input2 = "../model_data/vector_data/stationsC.shp"

	out1 = "../model_data/vector_data/meteo/meteoV"+str(month)+".shp"
	out2 = "../model_data/vector_data/meteo/meteoC"+str(month)+".shp"

	processing.runalg('qgis:joinattributestable', input1,tableV,'Estación','Estación',out1)
	processing.runalg('qgis:joinattributestable', input2,tableC,'Estación','Estación',out2)

	out = "../model_data/vector_data/meteo/meteo_"+str(month)+".shp"

	processing.runalg("qgis:mergevectorlayers",[out1,out2] , out)

csvV = "../model_data/meteo_data/testV.csv"
csvC = "../model_data/meteo_data/testC.csv"

QgsApplication.exitQgis() 

 


  
