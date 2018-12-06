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

# Function to process vector data (buffer, field, rasterize and reclass)
def vector(input,output,values,rules,name):
    
    buffer = []
    
    for i in range(len(values)):

        distance = values[i]
        out = "../model_data/vector_data/b/"+name+"_b_"+str(distance)+".shp"
        
        processing.runalg('qgis:fixeddistancebuffer', input, distance, 50, False, out)
        
        out1 = "../model_data/vector_data/f/"+name+"f"+str(distance)+".shp"
        
        processing.runalg('qgis:addfieldtoattributestable', out, "d", 1, 5, 0, out1)

	layer=QgsVectorLayer(out1,"l","ogr")
	QgsMapLayerRegistry.instance().addMapLayers([layer])

	features=layer.getFeatures()
	f=features.next()
	f.attributes()

	d=f.fields().indexFromName('d')

	layer.startEditing()
	for feat in features:
	  layer.changeAttributeValue(feat.id(), d, distance)

	layer.commitChanges()


input = "../model_data/vector_data/cities.shp"
name = "cities"
values = [300,600,900,1200,1500]

output = ""
rules = ""

vector(input,output,values,rules,name)

QgsApplication.exitQgis() 
