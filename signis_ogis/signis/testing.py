#Initialisierung und Beenden von QGIS in Python: 
#   Import modules 
import sys 
from qgis.core import * 
from qgis.gui import * 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from qgis.utils import * 
#    Configure QGIS directories and start the app 
#    Not to be used in QGIS python editor 
app = QgsApplication([], True) 
QgsApplication.setPrefixPath("/usr", True) 
QgsApplication.initQgis() 
sys.path.append("/usr/share/qgis/python/plugins")
import processing 
from processing.core.Processing import Processing 
from processing.tools import * 
Processing.initialize() 
# now do processing.runalg(...) - needs loaded Layer first
inputVectorFile = '/home/jorge/Escritorio/CCAA/Comunidades_Autonomas_ETRS89_30N.shp'
vecLayer = QgsVectorLayer(inputVectorFile, 'myVecLayer', 'ogr') 
processing.alghelp('grass:v.buffer.distance') 
processing.runalg('qgis:fixeddistancebuffer', vecLayer, 30, 10, False, '/tmp/buff.shp')
# ... 
# finish app at the end 
QgsApplication.exitQgis() 


