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

meteo = 1
firewalls = 0

if ((meteo == 1) or (firewalls == 1)):
	print "enter"
	if (meteo == 1):
		print "csv personalizado"

		if (firewalls == 1):
			print "firewalls personalizado"
		elif (firewalls == 0):
			print "firewalls :) "
	else:
		print "csv por defecto"

else:
 	print " :) "



QgsApplication.exitQgis() 

 


  
