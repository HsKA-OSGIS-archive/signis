#!/bin/bash

# SERVER SIGNIS
echo "Starting..."
cd signis_osgis
# source bin/activate
# echo "Virtual environment"
echo ""
echo "HELLO! I'm a software to start the signis application."
echo "Select an option: "
echo " 0 - Run server"
echo " 1 - Configure and run server"
while :
do
  read OPTION
  case $OPTION in
    0 )  echo "Nice! Let's start running the server...";
	cd signis
	python manage.py runserver;
	break;;
    1 )  echo "I will help you for the configuration.";
	echo "First, We need Django."
	# Building for DJANGO
	echo "Searching django..."
	{
	python -c "import django; print(django.get_version())";
	} || {
	echo "Not installed!"
	while true; do
	    read -p "Do you wish to install this program?" yn
	    case $yn in
		[Yy]* ) pip install django; break;;
		[Nn]* ) break;;
		* ) echo "Please answer yes or no.";;
	    esac
	done
	}
        echo ""
	cd signis
	cd signis
	# Global conf
	echo "For the configuration I need some ideas..."
	read -p "What's the postgres user? Write here: " namePostgres;
        read -sp "What's the postgres password? Write here: " passPostgres;
        echo ""
	echo "(Don't worry, this is not stored anywhere)"
	# Conf database
	while true; do
	    read -p "Do you wish to create a database?" yn
	    case $yn in
		[Yy]* ) echo "Nice";
			read -p  "The default database name is 'signis_osgis'. Write the same name if the database is called like 'signis_osgis' or put another name for the database:" databasePostgres;
			sudo -u $namePostgres createdb $databasePostgres;
			echo "Database created for user $namePostgres";
			break;;
		[Nn]* ) read -p  "Write the name of the database like 'signis_osgis' or put another name for your database:" databasePostgres;
			break;;
		* ) echo "Please answer yes or no.";;
	    esac
	done
	# Comment
	echo "So...the database name is $databasePostgres. Ok!";
	# Comment
	# Conf app connection
	while true; do
	    read -p "Do you wish to configure the application connection?" yn
	    case $yn in
		[Yy]* ) echo "Configuring application connection...";
			sed -i "85s/.*/        'NAME': '$databasePostgres',/" settings.py;
			sed -i "86s/.*/        'USER': '$namePostgres',/" settings.py;
			sed -i "87s/.*/        'PASSWORD': '$passPostgres',/" settings.py;
			echo "Application confidured for user $namePostgres"
			break;;
		[Nn]* ) break;;
		* ) echo "Please answer yes or no.";;
	    esac
	done
	# Comment
	echo "Well, Djando app has the references."
	echo "Let's start with the relations in the new database."
	# Comment
	cd ..
	# Migrate relations
	while true; do
	    read -p "Do you wish to migrate relations?" yn
	    case $yn in
		[Yy]* ) python manage.py migrate;
			break;;
		[Nn]* ) break;;
		* ) echo "Please answer yes or no.";;
	    esac
	done
	# Comment
	echo "The next step is to fill all the tables with the default data."
	# Comment
	while true; do
	    read -p "Do you wish to fill the tables?" yn
	    case $yn in
		[Yy]* ) echo "Restoring a backup and filling tables."
			sudo -u $namePostgres psql $databasePostgres < signis_osgis.backup;
			break;;
		[Nn]* ) break;;
		* ) echo "Please answer yes or no.";;
	    esac
	done
	# Comment
	echo "Oh yes! We have to post some layers in to the local geoserver."
	echo "I hope you have geoserver. If not, discard the following configuration, install geoserver and post the layers."
	# Comment
	# Conf GEOSERVER
	while true; do
	    read -p "Do you wish to configure GEOSERVER?" yn
	    case $yn in
		[Yy]* ) echo "So...tell me something";
			read -p "What's the geoserver user? Commonly is admin. Put the name here: " userGeoserver;
			read -sp "What's the geoserver password? Commonly is geoserver. Put the name here: " passGeoserver;
			echo ""
			echo "I can create a workspace in geoserver"
			read -p "The default workspace name is 'signis_osgis'. Write the same name:" workspaceGeoserver;
			curl -u $userGeoserver:$passGeoserver -v -POST -H 'Content-type:text/xml' -d '<workspace><name>'$workspaceGeoserver'</name></workspace>' http://localhost:8080/geoserver/rest/workspaces;
			echo "Workspace created in geoserver!";
			echo "I can create the store for the vectorial layers"
			read -p "The default store name is 'signis_osgis'. Write the same name:" storeGeoserver;
			echo "<dataStore><name>"$storeGeoserver"</name><connectionParameters><host>localhost</host><port>5432</port><database>"$databasePostgres"</database><schema>public</schema><user>"$namePostgres"</user><passwd>"$passPostgres"</passwd><dbtype>postgis</dbtype></connectionParameters></dataStore>" > $storeGeoserver".xml";
			nameFile=$storeGeoserver".xml";
			curl -v -u $userGeoserver:$passGeoserver -XPOST -T $nameFile -H 'Content-type: text/xml' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/datastores;
			# echo "Listing store..."
			# curl -v -u $userGeoserver:$passGeoserver -XGET http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/datastores/$nameFile
			echo "Publishing the layer firewalls..."
			curl -v -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d "<featureType><name>firewalls_firewalls</name></featureType>" http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/datastores/$storeGeoserver/featuretypes
			echo "Layer published"
			# Store to ImageMosaic
			echo "We have to create another store to manage the raster images."
			# read -p "The default store name is 'signis_osgis_model'. Write the same name if you want: " storeModelGeoserver;
			echo "Checking..."
			sudo chmod 777 -R ../../model/model_data/raster_data
			echo "Creating style...";
			curl -v -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d "<style><name>model_style</name><filename>raster_style.sld</filename></style>" http://localhost:8080/geoserver/rest/styles;
			curl -v -u $userGeoserver:$passGeoserver -XPUT -H "Content-type: application/vnd.ogc.sld+xml" -d @raster_style.sld http://localhost:8080/geoserver/rest/styles/model_style;
			cd ../../model/model_data/raster_data/signis_osgis_model
			path=$(pwd)
			echo "Publishing stores..."
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_january</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_january.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_february</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_february.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_march</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_march.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_april</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_april.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_may</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_may.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_juny</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_juny.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_july</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_july.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_august</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_august.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_september</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_september.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_october</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_october.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_november</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_november.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>default_model_december</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/default_model_december.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>own_model</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/own_model.tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores
			echo "Publishing layers..."
			latLonBoundingBox='<nativeBoundingBox><minx>656449.5752999996</minx><maxx>711524.5752999996</maxx><miny>4376198.7327</miny><maxy>4410048.7327</maxy></nativeBoundingBox><latLonBoundingBox><minx>5.896986867457583</minx><maxx>6.3917340101864095</maxx><miny>36.547343545100034</miny><maxy>36.791244229043</maxy><crs>EPSG:4326</crs></latLonBoundingBox>'

			curl -u $userGeoserver:$passGeoserver -XPOST -H 'Content-type: text/xml' -d '<coverage><name>default_model_january</name><title>default_model_january</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_january/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_february</name><title>default_model_february</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_february/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_march</name><title>default_model_march</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_march/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_april</name><title>default_model_april</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_april/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_may</name><title>default_model_may</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_may/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_juny</name><title>default_model_juny</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_juny/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_july</name><title>default_model_july</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_july/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_august</name><title>default_model_august</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_august/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_september</name><title>default_model_september</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_september/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_october</name><title>default_model_october</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_october/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_november</name><title>default_model_november</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_november/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>default_model_december</name><title>default_model_december</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/default_model_december/coverages
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d '<coverage><name>own_model</name><title>own_model</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/own_model/coverages
			
			cd ../../../../signis_osgis/signis
			echo "Raster image published!";
			# gdal_translate ../reclass/siose.tif siose20190108T180000000Z.tif
			
			break;;
		[Nn]* ) break;;
		* ) echo "Please answer yes or no.";;
	    esac
	done
	# Comment
	echo "The last step is to configure a superuser to log in."
	# Comment
	# Create superuser
	while true; do
	    read -p "Do you wish to create a super user?" yn
	    case $yn in
		[Yy]* ) python manage.py createsuperuser; break;;
		[Nn]* ) break;;
		* ) echo "Please answer yer or no.";;
	    esac
	done
	# Comment
	echo "NICE!"
	# Comment
	# Running server
	echo "Running server..."
	python manage.py runserver
	break;;
    * ) echo "Please answer 0 or 1.";;
  esac
done


