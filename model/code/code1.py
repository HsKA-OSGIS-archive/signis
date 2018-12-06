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
	print "buffer"
        
        out1 = "../model_data/vector_data/f/"+name+"f"+str(distance)+".shp"
        
        processing.runalg('qgis:addfieldtoattributestable', out, "d", 1, 5, 0, out1)
	print "field"

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
	print "field modifycd "

# 1 - cities
input1 = "../model_data/vector_data/cities.shp"
name1 = "cities"
values1 = [300,600,900,1200,1500]

# 2 - electric lines
input2 = "../model_data/vector_data/electric_lines.shp"
name2 = "electric_lines"
values2 = [30,60,90,120,150]

# 3 - roads
input3 = "../model_data/vector_data/roads.shp"
name3 = "roads"
values3 = [45,100,200]

# 4 - water
input4 = "../model_data/vector_data/water.shp"
name4 = "water"
values4 = [50,100,200,400]

# 5 - water
input5 = "../model_data/vector_data/water_points.shp"
name5 = "water_points"
values5 = [500,1000,1500,2000]

output = ""
rules = ""

#vector(input1,output,values1,rules,name1)
#vector(input2,output,values2,rules,name2)
#print "vector 2"
#vector(input3,output,values3,rules,name3)
#print "vector 3"
#vector(input4,output,values4,rules,name4)
#print "vector 4"
#vector(input5,output,values5,rules,name5)
#print "vector 5"

QgsApplication.exitQgis() 
