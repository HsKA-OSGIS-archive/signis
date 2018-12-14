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

def stations_join(tableC, tableV, month):

	input1 = "../model_data/vector_data/stationsV.shp"
	input2 = "../model_data/vector_data/stationsC.shp"

	out1 = "../model_data/vector_data/meteo/meteoV"+str(month)+".shp"
	out2 = "../model_data/vector_data/meteo/meteoC"+str(month)+".shp"

	processing.runalg('qgis:joinattributestable', input1,tableV,'Estación','Estación',out1)
	processing.runalg('qgis:joinattributestable', input2,tableC,'Estación','Estación',out2)

	out = "../model_data/vector_data/meteo/meteo_"+str(month)+".shp"

	processing.runalg("qgis:mergevectorlayers",[out1,out2] , out)

# January
tableV1 = "../model_data/meteo_data/1V.csv"
tableC1 = "../model_data/meteo_data/1C.csv"
month1 = 1;

# February
tableV2 = "../model_data/meteo_data/2V.csv"
tableC2 = "../model_data/meteo_data/2C.csv"
month2 = 2;

# March
tableV3 = "../model_data/meteo_data/3V.csv"
tableC3 = "../model_data/meteo_data/3C.csv"
month3 = 3;

# April
tableV4 = "../model_data/meteo_data/4V.csv"
tableC4 = "../model_data/meteo_data/4C.csv"
month4 = 4;

# May
tableV5 = "../model_data/meteo_data/5V.csv"
tableC5 = "../model_data/meteo_data/5C.csv"
month5 = 5;

# June
tableV6 = "../model_data/meteo_data/6V.csv"
tableC6 = "../model_data/meteo_data/6C.csv"
month6 = 6;

# July
tableV7 = "../model_data/meteo_data/7V.csv"
tableC7 = "../model_data/meteo_data/7C.csv"
month7 = 7;

# Agost
tableV8 = "../model_data/meteo_data/8V.csv"
tableC8 = "../model_data/meteo_data/8C.csv"
month8 = 8;

# September
tableV9 = "../model_data/meteo_data/9V.csv"
tableC9 = "../model_data/meteo_data/9C.csv"
month9 = 9;

# October
tableV10 = "../model_data/meteo_data/10V.csv"
tableC10 = "../model_data/meteo_data/10C.csv"
month10 = 10;

# November
tableV11 = "../model_data/meteo_data/11V.csv"
tableC11 = "../model_data/meteo_data/11C.csv"
month11 = 11;

# December
tableV12 = "../model_data/meteo_data/12V.csv"
tableC12 = "../model_data/meteo_data/12C.csv"
month12 = 12;

stations_join(tableC1, tableV1, month1)
stations_join(tableC2, tableV2, month2)
stations_join(tableC3, tableV3, month3)
stations_join(tableC5, tableV5, month5)
stations_join(tableC6, tableV6, month6)
stations_join(tableC7, tableV7, month7)
stations_join(tableC8, tableV8, month8)
stations_join(tableC9, tableV9, month9)
stations_join(tableC10, tableV10, month10)
stations_join(tableC11, tableV11, month11)
stations_join(tableC12, tableV12, month12)

QgsApplication.exitQgis() 
