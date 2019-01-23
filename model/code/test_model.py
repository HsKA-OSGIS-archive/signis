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

import csv

reload(sys)  
sys.setdefaultencoding('utf8')

Processing.initialize() 

def stations_join(tableC, tableV, month):

	input1 = "../model_data/vector_data/stationsV.shp"
	input2 = "../model_data/vector_data/stationsC.shp"

	out1 = "../model_data/vector_data/meteo/meteoV_user.shp"
	out2 = "../model_data/vector_data/meteo/meteoC_user.shp"

	processing.runalg('qgis:joinattributestable', input1,tableV,'Estación','Estación',out1)
	processing.runalg('qgis:joinattributestable', input2,tableC,'Estación','Estación',out2)

	out = "../model_data/vector_data/meteo/meteo_user.shp"

	processing.runalg("qgis:mergevectorlayers",[out1,out2] , out)

def station_interpolation(input):

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

		out1 = "../model_data/raster_data/IDW/"+name+"_user.tif"

		processing.runalg('saga:inversedistanceweighted', input,field,1,2.0,False,1.0,1,100.0,0,-1.0,10.0,0,0,10.0,"%f,%f,%f,%f" %(xmin, xmax, ymin, ymax),100.0,0,0,None,3,out1)

		rules = "../model_data/rules/"+name+".txt"
		out2 = "../model_data/raster_data/reclass/"+name+"_user.tif"

		processing.runalg("grass7:r.reclass", out1,rules, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, out2)
meteo = 0
firewalls = 0

if ((meteo == 1) or (firewalls == 1)):

	if (meteo == 1):
		print "csv personalizado"
		# CVS files
		csvV = "../model_data/meteo_data/testV.csv"
		csvC = "../model_data/meteo_data/testC.csv"

		# Look for the month
		cont = 1;
		reader = csv.reader(open(csvV,'rb'))
		for row in (reader):
			if cont == 2:
				month = row[0].split(';')[3]
			cont = cont + 1

		# join tables
		#stations_join(csvC, csvV, month)

		# Interpolation
		#input = "../model_data/vector_data/meteo/meteo_user.shp"
		#station_interpolation(input)

		# Take NDVI depending on the month
		season = "none"

		if (('4' in month) or ('5' in month) or ('6' in month)):
			season = "spring"
		elif (('7' in month) or ('8' in month) or ('9' in month)):
			season = "summer"
		elif (('10' in month) or ('11' in month) or ('12' in month)):
			season = "autumn"
		elif (('1' in month) or ('2' in month) or ('3' in month)):
			season = "winter"
			
		#print season

		if (firewalls == 1):
			print "firewalls personalizado"
		elif (firewalls == 0):
			print "firewalls :) "
	else:

		print "csv :) "
		if (firewalls == 1):
			print "firewalls personalizado"
		elif (firewalls == 0):
			print "firewalls :) "

else:
 	print " :) "



QgsApplication.exitQgis() 

 


  
