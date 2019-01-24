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
    merge = []
    
    for i in range(len(values)):

	val = []
        distance = values[i]
        out = "../model_data/vector_data/b/"+name+"_b_"+str(distance)+".shp"
        
        processing.runalg('qgis:fixeddistancebuffer', input, distance, 50, True, out)
	print "buffer"
        
        out1 = "../model_data/vector_data/f/"+name+"_f_"+str(distance)+".shp"
        
        processing.runalg('qgis:addfieldtoattributestable', out, "d", 1, 10, 5, out1)
	print "field"

	layer=QgsVectorLayer(out1,"l","ogr")
	QgsMapLayerRegistry.instance().addMapLayers([layer])

	features=layer.getFeatures()

	layer.startEditing()
	for feat in features:
	  d = feat.fieldNameIndex("d")
	  layer.changeAttributeValue(feat.id(), d, distance)
		
	layer.commitChanges()
	print "field modified"

	val.append(distance)
	val.append(out1)
	buffer.append(val)

    for j in range(len(buffer)-1):
	print "enter"
	dis = buffer[j+1][0]
	input1 = buffer[j][1]
	input2 = buffer[j+1][1]
	print dis, input1, input2
	out2="../model_data/vector_data/d/"+name+"_d_"+str(dis)+".shp"
        
        processing.runalg('qgis:difference', input2, input1, True, out2)
	merge.append(out2)

    out3 = "../model_data/vector_data/m/"+name+"_m.shp"

    merge.append(buffer[0][1])
    processing.runalg('qgis:mergevectorlayers', merge,out3)
    print "merged"
     
    out4 = "../model_data/raster_data/raw/"+name+".tif"

    layer=QgsVectorLayer(out3,"l","ogr")
    QgsMapLayerRegistry.instance().addMapLayers([layer])

    extent = layer.extent()
    xmin = extent.xMinimum()
    xmax = extent.xMaximum()
    ymin = extent.yMinimum()
    ymax = extent.yMaximum()

    processing.runalg('gdalogr:rasterize', out3,'d',1,10.0,10.0,"%f,%f,%f,%f" %(xmin, xmax, ymin, ymax),False,5,None,4,75.0,6.0,1.0,False,2,None,out4)
    print "rasterized"

    out5 = "../model_data/raster_data/reclass/"+name+".tif"
    processing.runalg("grass7:r.reclass", out4,rules, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, out5)
    print "reclassified"

# 1 - cities
input1 = "../model_data/vector_data/cities.shp"
name1 = "cities"
values1 = [300,600,900,1200,1500]
rules1 = "../model_data/rules/cities.txt"

# 2 - electric lines
input2 = "../model_data/vector_data/electric_lines.shp"
name2 = "electric_lines"
values2 = [30,60,90,120,150]
rules2 = "../model_data/rules/electric_lines.txt"

# 3 - roads
input3 = "../model_data/vector_data/roads2.shp"
name3 = "roads"
values3 = [45,100,200]
rules3 = "../model_data/rules/roads.txt"

# 4 - water
input4 = "../model_data/vector_data/water.shp"
name4 = "water"
values4 = [50,100,200,400]
rules4 = "../model_data/rules/water.txt"

# 5 - water points
input5 = "../model_data/vector_data/water_points.shp"
name5 = "water_points"
values5 = [500,1000,1500,2000]
rules5 = "../model_data/rules/water_points.txt"

# 6 - Firewalls
input6 = "../model_data/vector_data/firewalls.shp"
name6 = "firewalls"
values6 = [10,15]
rules6 = "../model_data/rules/firewalls.txt"

# 7 - Roads_firewalls
input7 = "../model_data/vector_data/roads.shp"
name7 = "roads_firewalls"
values7 = [5,10]
rules7 = "../model_data/rules/roads_firewalls.txt"

# 8 - rivers
input8 = "../model_data/vector_data/rivers2.shp"
name8 = "rivers"
values8 = [5,10]
rules8 = "../model_data/rules/rivers.txt"

output = ""
rules = ""

#vector(input1,output,values1,rules1,name1)
#print "vector 1"
#vector(input2,output,values2,rules2,name2)
#print "vector 2"
vector(input3,output,values3,rules3,name3)
print "vector 3"
#vector(input4,output,values4,rules4,name4)
#print "vector 4"
#vector(input5,output,values5,rules5,name5)
#print "vector 5"
#vector(input6,output,values6,rules6,name6)
#print "vector 6"
#vector(input7,output,values7,rules7,name7)
#print "vector 7"
#vector(input8,output,values8,rules8,name8)
#print "vector 8"

QgsApplication.exitQgis() 
