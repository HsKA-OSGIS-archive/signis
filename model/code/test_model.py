# coding=utf-8

#   Import modules 
import sys 
from qgis.core import * 
from qgis.gui import * 
from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from qgis.utils import * 
from django.conf import settings
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
from qgis.analysis import *

import sys,os
#import pandas as pd

import csv

reload(sys)  
sys.setdefaultencoding('utf8')

settingsUser = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
name = settings.DATABASES['default']['NAME']

#print user, password, name

def runModel(meteo,firewalls_input,m):

	Processing.initialize() 

	def vector(input,values):
	    
	    buffer = []
	    merge = []
		
            rules = "../../model/model_data/rules/firewalls.txt"
	    zone = "../../model/model_data/vector_data/work_zone.shp"
	    
	    for i in range(len(values)):

		val = []
		distance = values[i]
		out = "../../model/model_data/vector_data/b/user_b_"+str(distance)+".shp"
		
		processing.runalg('qgis:fixeddistancebuffer', input, distance, 50, True, out)
		print "buffer"
		
		out1 = "../../model/model_data/vector_data/f/user_f_"+str(distance)+".shp"
		
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
		out2="../../model/model_data/vector_data/d/user_d_"+str(dis)+".shp"
		
		processing.runalg('qgis:difference', input2, input1, True, out2)
		merge.append(out2)

	    out3 = "../../model/model_data/vector_data/m/user_m.shp"

	    merge.append(buffer[0][1])
	    processing.runalg('qgis:mergevectorlayers', merge,out3)
	    print "merged"
	     
	    out4 = "../../model/model_data/raster_data/raw/firewalls_user.tif"

	    layer2=QgsVectorLayer(zone,"l","ogr")
	    QgsMapLayerRegistry.instance().addMapLayers([layer2])

	    extent = layer2.extent()
	    xmin = extent.xMinimum()
	    xmax = extent.xMaximum()
	    ymin = extent.yMinimum()
	    ymax = extent.yMaximum()

	    processing.runalg('gdalogr:rasterize', out3,'d',1,10.0,10.0,"%f,%f,%f,%f" %(xmin, xmax, ymin, ymax),False,5,None,4,75.0,6.0,1.0,False,2,None,out4)

	    print "rasterized"

	    out5 = "../../model/model_data/raster_data/reclass/firewalls_user.tif"
	    processing.runalg("grass7:r.reclass", out4,rules, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, out5)

	    print "reclassified"

	def stations_join(tableC, tableV, month):

		input1 = "../../model/model_data/vector_data/stationsV.shp"
		input2 = "../../model/model_data/vector_data/stationsC.shp"

		out1 = "../../model/model_data/vector_data/meteo/meteoV_user.shp"
		out2 = "../../model/model_data/vector_data/meteo/meteoC_user.shp"

		processing.runalg('qgis:joinattributestable', input1,tableV,'Estación','Estación',out1)
		processing.runalg('qgis:joinattributestable', input2,tableC,'Estación','Estación',out2)

		out = "../../model/model_data/vector_data/meteo/meteo_user.shp"

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

			out1 = "../../model/model_data/raster_data/IDW/"+name+"_user.tif"

			processing.runalg('saga:inversedistanceweighted', input,field,1,2.0,False,1.0,1,100.0,0,-1.0,10.0,0,0,10.0,"%f,%f,%f,%f" %(xmin, xmax, ymin, ymax),100.0,0,0,None,3,out1)

			rules = "../../model/model_data/rules/"+name+".txt"
			out2 = "../../model/model_data/raster_data/reclass/"+name+"_user.tif"

			processing.runalg("grass7:r.reclass", out1,rules, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, out2)

	slope = "../../model/model_data/raster_data/reclass/slope.tif"
	siose = "../../model/model_data/raster_data/reclass/siose.tif"
	orientation = "../../model/model_data/raster_data/reclass/orientation.tif"
	rivers = "../../model/model_data/raster_data/reclass/rivers.tif"
	water = "../../model/model_data/raster_data/reclass/water.tif"
	water_points = "../../model/model_data/raster_data/reclass/water_points.tif"
	electric_lines = "../../model/model_data/raster_data/reclass/electric_lines.tif"
	cities = "../../model/model_data/raster_data/reclass/cities.tif"
	ilumination = "../../model/model_data/raster_data/reclass/ilumination.tif"
	roads = "../../model/model_data/raster_data/reclass/roads.tif"
	rules2 = "../../model/model_data/rules/model.txt"

	input_slope = QgsRasterLayer(slope,'slope')
	input_siose = QgsRasterLayer(siose,'siose')
	input_orientation = QgsRasterLayer(orientation,'orientation')
	input_rivers = QgsRasterLayer(rivers,'rivers')
	input_water = QgsRasterLayer(water,'water')
	input_water_points = QgsRasterLayer(water_points,'water_points')
	input_electric_lines = QgsRasterLayer(electric_lines,'electric_lines')
	input_cities = QgsRasterLayer(cities,'cities')
	input_ilumination = QgsRasterLayer(ilumination,'ilumination')
	input_roads = QgsRasterLayer(roads,'roads')

	entries = []

	raster0 = QgsRasterCalculatorEntry()
	raster0.ref="input0@1"
	raster0.raster = input_slope
	raster0.bandNumber = 1
	entries.append(raster0)

	raster1 = QgsRasterCalculatorEntry()
	raster1.ref="input1@1"
	raster1.raster = input_siose
	raster1.bandNumber = 1
	entries.append(raster1)

	raster2 = QgsRasterCalculatorEntry()
	raster2.ref="input2@1"
	raster2.raster = input_orientation
	raster2.bandNumber = 1
	entries.append(raster2)

	raster3 = QgsRasterCalculatorEntry()
	raster3.ref="input3@1"
	raster3.raster = input_rivers
	raster3.bandNumber = 1
	entries.append(raster3)

	raster4 = QgsRasterCalculatorEntry()
	raster4.ref="input4@1"
	raster4.raster = input_water
	raster4.bandNumber = 1
	entries.append(raster4)

	raster5 = QgsRasterCalculatorEntry()
	raster5.ref="input5@1"
	raster5.raster = input_water_points
	raster5.bandNumber = 1
	entries.append(raster5)

	raster6 = QgsRasterCalculatorEntry()
	raster6.ref="input6@1"
	raster6.raster = input_electric_lines
	raster6.bandNumber = 1
	entries.append(raster6)

	raster7 = QgsRasterCalculatorEntry()
	raster7.ref="input7@1"
	raster7.raster = input_cities
	raster7.bandNumber = 1
	entries.append(raster7)

	raster8 = QgsRasterCalculatorEntry()
	raster8.ref="input8@1"
	raster8.raster = input_ilumination
	raster8.bandNumber = 1
	entries.append(raster8)

	raster9 = QgsRasterCalculatorEntry()
	raster9.ref="input9@1"
	raster9.raster = input_roads
	raster9.bandNumber = 1
	entries.append(raster9)
	print "primeras capas cargadas"

	if ((meteo == 1) or (firewalls_input == 1)):

		if (meteo == 1):
			print "csv personalizado"
			# CVS files
			csvV = "../../model/model_data/meteo_data/userV.csv"
			csvC = "../../model/model_data/meteo_data/userC.csv"

			# Look for the month
			cont = 1;
			reader = csv.reader(open(csvV,'rb'))
			for row in (reader):
				if cont == 2:
					month = row[0].split(';')[3]
				cont = cont + 1

			# join tables
			stations_join(csvC, csvV, month)

			# Interpolation
			input = "../../model/model_data/vector_data/meteo/meteo_user.shp"
			station_interpolation(input)

			# Take NDVI depending on the month
			season = "none"

			if (('4' in month) or ('5' in month) or ('6' in month)):
				ndvi = "../../model/model_data/raster_data/reclass/NDVI_spring.tif"
			elif (('7' in month) or ('8' in month) or ('9' in month)):
				ndvi = "../../model/model_data/raster_data/reclass/NDVI_summer.tif"
			elif (('10' in month) or ('11' in month) or ('12' in month)):
				ndvi = "../../model/model_data/raster_data/reclass/NDVI_autumn.tif"
			elif (('1' in month) or ('2' in month) or ('3' in month)):
				ndvi = "../../model/model_data/raster_data/reclass/NDVI_winter.tif"
				
			print ndvi

			if (firewalls_input == 1):
				print "firewalls personalizado"
				uri = QgsDataSourceURI ()
				uri.setConnection ("localhost","5432",name,settingsUser,password)
				uri.setDataSource ("public","firewalls_firewalls","geom")
				firewalls_v = QgsVectorLayer ( uri.uri (), "firewalls","postgres")
				vector(firewalls_v,[10,15])
				firewalls = "../../model/model_data/raster_data/reclass/firewalls_user.tif"

			elif (firewalls_input == 0):
				print "firewalls :) "
				firewalls = "../../model/model_data/raster_data/reclass/firewalls.tif"

			temperature = "../../model/model_data/raster_data/reclass/temperature_user.tif"
			precipitations = "../../model/model_data/raster_data/reclass/precipitations_user.tif"
			humidity = "../../model/model_data/raster_data/reclass/humidity_user.tif"
			wind = "../../model/model_data/raster_data/reclass/wind_user.tif"

			input_temperature = QgsRasterLayer(temperature,'temperature')
			input_precipitations = QgsRasterLayer(precipitations,'precipitations')
			input_humidity = QgsRasterLayer(humidity,'humidity')
			input_wind = QgsRasterLayer(wind,'wind')
			input_ndvi = QgsRasterLayer(ndvi,'ndvi')
			input_firewalls = QgsRasterLayer(firewalls,'firewalls')

			raster10 = QgsRasterCalculatorEntry()
			raster10.ref="input10@1"
			raster10.raster = input_temperature
			raster10.bandNumber = 1
			entries.append(raster10)

			raster11 = QgsRasterCalculatorEntry()
			raster11.ref="input11@1"
			raster11.raster = input_precipitations
			raster11.bandNumber = 1
			entries.append(raster11)

			raster12 = QgsRasterCalculatorEntry()
			raster12.ref="input12@1"
			raster12.raster = input_humidity
			raster12.bandNumber = 1
			entries.append(raster12)

			raster13 = QgsRasterCalculatorEntry()
			raster13.ref="input13@1"
			raster13.raster = input_wind
			raster13.bandNumber = 1
			entries.append(raster13)

			raster14 = QgsRasterCalculatorEntry()
			raster14.ref="input14@1"
			raster14.raster = input_ndvi
			raster14.bandNumber = 1
			entries.append(raster14)

			raster15 = QgsRasterCalculatorEntry()
			raster15.ref="input15@1"
			raster15.raster = input_firewalls
			raster15.bandNumber = 1
			entries.append(raster15)
			print "segundas capas cargadas"
			output_ignition_risk = "../../model/results/ignition_risk_user.tif"

			calc = QgsRasterCalculator('(4*((input6@1 + input7@1 + input9@1)/3))+(3*((input14@1 + input10@1 + input11@1)/3))+(input8@1)', output_ignition_risk, "GTiff", input_siose.extent(), input_siose.width(), input_siose.height(), entries)

			calc.processCalculation()
			print "calculado1"
			output_propagation_risk = "../../model/results/propagation_risk_user.tif"

			calc2 = QgsRasterCalculator('(5*(input1@1)) + (4*((input0@1+input13@1)/2)) + (3*(input2@1)) - ((input3@1+input15@1)+((0.6*input5@1)+(0.4*input4@1))) - (input12@1)', output_propagation_risk, "GTiff", input_siose.extent(), input_siose.width(), input_siose.height(), entries)

			calc2.processCalculation()
			print "calculado 2"

			in1 = QgsRasterLayer(output_propagation_risk,'in1')
			in2 = QgsRasterLayer(output_ignition_risk,'in2')

			entriesin = []

			rasterin1 = QgsRasterCalculatorEntry()
			rasterin1.ref="in1@1"
			rasterin1.raster = in1
			rasterin1.bandNumber = 1
			entriesin.append(rasterin1)

			rasterin2 = QgsRasterCalculatorEntry()
			rasterin2.ref="in2@1"
			rasterin2.raster = in2
			rasterin2.bandNumber = 1
			entriesin.append(rasterin2)
			
			output_risk = "../../model/results/risk_user.tif"

			calc3 = QgsRasterCalculator('in1@1+in2@1', output_risk, "GTiff", in1.extent(), in1.width(), in1.height(), entriesin)

			calc3.processCalculation()

			la = "../../model/model_data/vector_data/work_zone.shp"
			layer=QgsVectorLayer(la,"l","ogr")
			QgsMapLayerRegistry.instance().addMapLayers([layer])

			extent = layer.extent()
			xmin = extent.xMinimum()
			xmax = extent.xMaximum()
			ymin = extent.yMinimum()
			ymax = extent.yMaximum()

			output_risk_reclass = "../../model/results/final/risk_user.tif"

			processing.runalg("grass7:r.reclass", output_risk,rules2, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, output_risk_reclass)
			print "reclass"

		else:
			if ((4 == m) or (5 == m) or (6 == m)):
				ndvi = "../../model/model_data/raster_data/reclass/NDVI_spring.tif"
			elif ((7 == m) or (8 == m) or (9 == m)):
				ndvi = "../../model/model_data/raster_data/reclass/NDVI_summer.tif"
			elif ((10 == m) or (11 == m) or (12 == m)):
				ndvi = "../../model/model_data/raster_data/reclass/NDVI_autumn.tif"
			elif ((1 == m) or (2 == m) or (3 == m)):
				ndvi = "../../model/model_data/raster_data/reclass/NDVI_winter.tif"
			print ndvi

			print "csv :) "
			if (firewalls_input == 1):
				print "firewalls personalizado"
				uri = QgsDataSourceURI ()
				uri.setConnection ("localhost","5432",name,settingsUser,password)
				uri.setDataSource ("public","firewalls_firewalls","geom")
				firewalls_v = QgsVectorLayer ( uri.uri (), "firewalls","postgres")
				vector(firewalls_v,[10,15])
				firewalls = "../../model/model_data/raster_data/reclass/firewalls_user.tif"


			elif (firewalls_input == 0):
				print "firewalls :) "
				firewalls = "../../model/model_data/raster_data/reclass/firewalls.tif"

			temperature = "../../model/model_data/raster_data/reclass/temperature_"+str(m)+".tif"
			precipitations = "../../model/model_data/raster_data/reclass/precipitations_"+str(m)+".tif"
			humidity = "../../model/model_data/raster_data/reclass/humidity_"+str(m)+".tif"
			wind = "../../model/model_data/raster_data/reclass/wind_"+str(m)+".tif"

			input_temperature = QgsRasterLayer(temperature,'temperature')
			input_precipitations = QgsRasterLayer(precipitations,'precipitations')
			input_humidity = QgsRasterLayer(humidity,'humidity')
			input_wind = QgsRasterLayer(wind,'wind')
			input_ndvi = QgsRasterLayer(ndvi,'ndvi')
			input_firewalls = QgsRasterLayer(firewalls,'firewalls')

			raster10 = QgsRasterCalculatorEntry()
			raster10.ref="input10@1"
			raster10.raster = input_temperature
			raster10.bandNumber = 1
			entries.append(raster10)

			raster11 = QgsRasterCalculatorEntry()
			raster11.ref="input11@1"
			raster11.raster = input_precipitations
			raster11.bandNumber = 1
			entries.append(raster11)

			raster12 = QgsRasterCalculatorEntry()
			raster12.ref="input12@1"
			raster12.raster = input_humidity
			raster12.bandNumber = 1
			entries.append(raster12)

			raster13 = QgsRasterCalculatorEntry()
			raster13.ref="input13@1"
			raster13.raster = input_wind
			raster13.bandNumber = 1
			entries.append(raster13)

			raster14 = QgsRasterCalculatorEntry()
			raster14.ref="input14@1"
			raster14.raster = input_ndvi
			raster14.bandNumber = 1
			entries.append(raster14)

			raster15 = QgsRasterCalculatorEntry()
			raster15.ref="input15@1"
			raster15.raster = input_firewalls
			raster15.bandNumber = 1
			entries.append(raster15)
			print "segundas capas cargadas"
			output_ignition_risk = "../../model/results/ignition_risk_user.tif"

			calc = QgsRasterCalculator('(4*((input6@1 + input7@1 + input9@1)/3))+(3*((input14@1 + input10@1 + input11@1)/3))+(input8@1)', output_ignition_risk, "GTiff", input_siose.extent(), input_siose.width(), input_siose.height(), entries)

			calc.processCalculation()
			print "calculado1"
			output_propagation_risk = "../../model/results/propagation_risk_user.tif"

			calc2 = QgsRasterCalculator('(5*(input1@1)) + (4*((input0@1+input13@1)/2)) + (3*(input2@1)) - ((input3@1+input15@1)+((0.6*input5@1)+(0.4*input4@1))) - (input12@1)', output_propagation_risk, "GTiff", input_siose.extent(), input_siose.width(), input_siose.height(), entries)

			calc2.processCalculation()
			print "calculado 2"

			in1 = QgsRasterLayer(output_propagation_risk,'in1')
			in2 = QgsRasterLayer(output_ignition_risk,'in2')

			entriesin = []

			rasterin1 = QgsRasterCalculatorEntry()
			rasterin1.ref="in1@1"
			rasterin1.raster = in1
			rasterin1.bandNumber = 1
			entriesin.append(rasterin1)

			rasterin2 = QgsRasterCalculatorEntry()
			rasterin2.ref="in2@1"
			rasterin2.raster = in2
			rasterin2.bandNumber = 1
			entriesin.append(rasterin2)
			
			output_risk = "../../model/results/risk_user.tif"

			calc3 = QgsRasterCalculator('in1@1+in2@1', output_risk, "GTiff", in1.extent(), in1.width(), in1.height(), entriesin)

			calc3.processCalculation()

			la = "../../model/model_data/vector_data/work_zone.shp"
			layer=QgsVectorLayer(la,"l","ogr")
			QgsMapLayerRegistry.instance().addMapLayers([layer])

			extent = layer.extent()
			xmin = extent.xMinimum()
			xmax = extent.xMaximum()
			ymin = extent.yMinimum()
			ymax = extent.yMaximum()

			output_risk_reclass = "../../model/results/final/risk_user.tif"
			
			processing.runalg("grass7:r.reclass", output_risk,rules2, "", "%f,%f,%f,%f"% (xmin, xmax, ymin, ymax), 0, output_risk_reclass)

			print "reclass"
	else:
	 	print " :) "


	#QgsApplication.exitQgis()
	return 'model created'

if __name__== '__main__':
    runModel(0,1,7)




  
