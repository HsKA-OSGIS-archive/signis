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

Processing.initialize() 

#file = os.getcwd()
#file2 = os.path.dirname('./')
#file3 = os.path.realpath('.')
#print file3
#path = "./"+file
#print path

data = "/home/user/OSGIS/signis/model/model_data/vector_data/cities.shp"
output1 = "/home/user/OSGIS/signis/model/model_data/vector_data/b/b300.shp"
output2 = "/home/user/OSGIS/signis/model/model_data/vector_data/f/f300.shp"
output3 = "/home/user/OSGIS/signis/model/model_data/vector_data/fv/fv300.shp"
distance = 300

layer = QgsVectorLayer(output1,'','ogc')

#for feature in layer.getFeatures():
#	feature.setAttribute("d",300)
#	print "."

print "enter"
processing.runalg('qgis:fixeddistancebuffer', data, distance, 50, False, output1)
print "buffer created"
processing.runalg('qgis:addfieldtoattributestable', output1, 'd', 1, 5, 0, output2)
print "field created"
processing.runalg('qgis:fieldcalculator', output2, 'd', 1, 5, 0, True, "$area", output3)
#processing.runalg('qgis:advancedpythonfieldcalculator', output2, "d", 1, 5, 0, '', distance, output3)
#print "field value"

#processing.runalg("qgis:refactorfields",output2, [{ 'name': 'd', 'type':1, 'length':5, 'precision':0, 'expression':distance},{ 'name': 'ETIQUETA', 'type':2, 'length':30, 'precision':0, 'expression':0}],output3)




QgsApplication.exitQgis() 

 


  
