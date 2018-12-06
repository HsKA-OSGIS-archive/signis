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

input_layer = "/home/user/OSGIS/signis/model/model_data/vector_data/f/f300.shp"
output = "/home/user/OSGIS/signis/model/model_data/vector_data/fv/fv300.shp"

distance = 300

#processing.runalg('qgis:fieldcalculator', input, "d", 1, 5, 0, False, distance, output)
#processing.runalg('qgis:fieldcalculator', input_layer, 'd', 1, 5, 0, True, 300, output)
#processing.runalg('qgis:fieldcalculator', input_layer,'d',0,10.0,3.0,True,'300',output)

layer=QgsVectorLayer(input_layer,"l","ogr")
QgsMapLayerRegistry.instance().addMapLayers([layer])


#####Attribut aus Shape abfragen

features=layer.getFeatures()
f=features.next()
f.attributes()

##Index von bestimmten Spaltennamen finden um den später ansprechen zu können (ANB beinhaltet dann Index als Zahl) 
d=f.fields().indexFromName('d')

## nur ein bestimmtes Attribut aus einer Spalte auswählen und anzeigen lassen
#selection=layer.getFeatures(QgsFeatureRequest().setFilterExpression(u' "ANB"=2'))

## selektierte Werte updaten:

layer.startEditing()
for feat in features:
  layer.changeAttributeValue(feat.id(), d, 3)

layer.commitChanges()


QgsApplication.exitQgis() 

 


  
