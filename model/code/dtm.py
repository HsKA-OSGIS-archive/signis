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

#input = "../model_data/DTM/"
#output1 = "../model_data/DTM/slope/"
#processing.runalg('gdalogr:slope', input, band, compute_edges, zevenbergen, as_percent, scale, output1)

QgsApplication.exitQgis() 
