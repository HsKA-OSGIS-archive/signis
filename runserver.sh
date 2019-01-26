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
    1 )  echo -ne "I will help you for the configuration. \n";
	echo -ne '                           (00%)\n'
	echo -ne "First, We need Django."
	# Building for DJANGO
	echo -ne "Searching django..."
	{
	python -c "import django; print(django.get_version())";
	} || {
	echo -ne "Not installed!"
	while true; do
	    read -p "Do you wish to install this program?" yn
	    case $yn in
		[Yy]* ) pip install django; break;;
		[Nn]* ) break;;
		* ) echo -ne "Please answer yes or no.";;
	    esac
	done
	}
	echo -ne '\n#####                    (10%)\n'
	sleep 1
        echo -ne ""
	cd signis
	cd signis
	# Global conf
	echo -ne "For the configuration I need some ideas..."
	echo -ne "(Don't worry, this is not stored anywhere)\n"
	read -p "What's the postgres user? Write here: " namePostgres;
        read -sp "What's the postgres password? Write here: " passPostgres;
	echo -ne '\n#######                  (15%)\n'
        echo -ne ""
	sleep 1
	# Conf database
	while true; do
	    read -p "Do you wish to create a database?" yn
	    case $yn in
		[Yy]* ) echo -ne "Nice";
			read -p  "The default database name is 'signis_osgis'. Press enter for default value 'signis_osgis' or put another name for the database:" databasePostgres;
			databasePostgres=${databasePostgres:-signis_osgis}
			sudo -u $namePostgres createdb $databasePostgres;
			echo -ne "Database $databasePostgres created for user $namePostgres";
			break;;
		[Nn]* ) read -p  "Press enter for default value 'signis_osgis' or put another name for your database:" databasePostgres;
			databasePostgres=${databasePostgres:-signis_osgis}
			break;;
		* ) echo -ne "Please answer yes or no.";;
	    esac
	done
	# Comment
	echo -ne "So...the database name is $databasePostgres. Ok!";
	echo -ne '\n########                 (20%)\n'
	sleep 0.5
	# Comment
	# Conf app connection
	while true; do
	    read -p "Do you wish to configure the application connection?" yn
	    case $yn in
		[Yy]* ) echo -ne "Configuring application connection...\n";
			sed -i "84s/.*/        'NAME': '$databasePostgres',/" settings.py;
			sed -i "85s/.*/        'USER': '$namePostgres',/" settings.py;
			sed -i "86s/.*/        'PASSWORD': '$passPostgres',/" settings.py;
			echo -ne "Application confidured for user $namePostgres"
			break;;
		[Nn]* ) break;;
		* ) echo -ne "Please answer yes or no.";;
	    esac
	done
	# Comment
	echo -ne "\nWell, Djando app has the references."
	echo -ne '\n##########               (30%)\n'
	sleep 0.5
	echo -ne "Let's start with the relations in the new database.\n"
	# Comment
	cd ..
	# Migrate relations
	while true; do
	    read -p "Do you wish to migrate relations?" yn
	    case $yn in
		[Yy]* ) python manage.py migrate;
			break;;
		[Nn]* ) break;;
		* ) echo -ne "Please answer yes or no.";;
	    esac
	done
	# Comment
	echo -ne '\n###########              (35%)\n'
	echo -ne "The next step is to fill all the tables with the default data.\n"
	# Comment
	while true; do
	    read -p "Do you wish to fill the tables?" yn
	    case $yn in
		[Yy]* ) echo -ne "Restoring a backup and filling tables."
			sudo -u $namePostgres psql $databasePostgres < signis_osgis.backup;
			break;;
		[Nn]* ) break;;
		* ) echo -ne "Please answer yes or no.";;
	    esac
	done
	# Comment
	echo -ne '\n############             (40%)\n'
	sleep 0.5
	echo -ne "Oh yes! We have to post some layers in to the local geoserver.\n"
	echo -ne "I hope you have geoserver. If not, discard the following configuration, install geoserver and post the layers.\n"
	sleep 0.5
	# Comment
	# Conf GEOSERVER
	while true; do
	    read -p "Do you wish to configure GEOSERVER?" yn
	    case $yn in
		[Yy]* ) echo -ne "So...tell me something\n";
			read -p "What's the geoserver user? Commonly is admin. Press enter for default or write another: \n" userGeoserver;
			userGeoserver=${userGeoserver:-admin}
			read -sp "What's the geoserver password? Commonly is geoserver. Press enter for default or write another: \n" passGeoserver;
			passGeoserver=${passGeoserver:-geoserver}
			echo -ne '\n##############           (50%)\n'
			sleep 0.5
			echo -ne ""
			echo -ne "I can create a workspace in geoserver\n"
			read -p "The default workspace name is 'signis_osgis'. Press enter for default or write another:" workspaceGeoserver;
			workspaceGeoserver=${workspaceGeoserver:-signis_osgis}
			curl -u $userGeoserver:$passGeoserver -POST -H 'Content-type:text/xml' -d '<workspace><name>'$workspaceGeoserver'</name></workspace>' http://localhost:8080/geoserver/rest/workspaces;
			echo -ne "\nWorkspace created in geoserver!";
			echo -ne '\n###############          (55%)\n'
			sleep 0.5
			echo -ne "I can create the store for the vectorial layers\n"
			read -p "The default store name is 'signis_osgis'. Write the same name:" storeGeoserver;
			storeGeoserver=${storeGeoserver:-signis_osgis}
			echo -ne "<dataStore><name>"$storeGeoserver"</name><connectionParameters><host>localhost</host><port>5432</port><database>"$databasePostgres"</database><schema>public</schema><user>"$namePostgres"</user><passwd>"$passPostgres"</passwd><dbtype>postgis</dbtype></connectionParameters></dataStore>" > $storeGeoserver".xml";
			nameFile=$storeGeoserver".xml";
			curl -u $userGeoserver:$passGeoserver -XPOST -T $nameFile -H 'Content-type: text/xml' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/datastores;
			# echo "Listing store..."
			# curl -u $userGeoserver:$passGeoserver -XGET http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/datastores/$nameFile
			echo -ne "\nPublishing the layer firewalls..."
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d "<featureType><name>firewalls_firewalls</name></featureType>" http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/datastores/$storeGeoserver/featuretypes
			echo -ne "\nLayer published"
			echo -ne '\n#################        (65%)\n'
			sleep 0.5
			# Store to ImageMosaic
			echo -ne "We have to create another store to manage the raster images."
			# read -p "The default store name is 'signis_osgis_model'. Write the same name if you want: " storeModelGeoserver;
			echo -ne "\nChecking...\n"
			sudo chmod 777 -R ../../model/model_data/raster_data
			echo -ne "Creating raster style...";
			curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-type: text/xml" -d "<style><name>model_style</name><filename>raster_style.sld</filename></style>" http://localhost:8080/geoserver/rest/styles;
			curl -u $userGeoserver:$passGeoserver -XPUT -H "Content-type: application/vnd.ogc.sld+xml" -d @raster_style.sld http://localhost:8080/geoserver/rest/styles/model_style;
			echo -ne '\n##################       (67%)\n'
			sleep 0.5
			cd ../../model/results/final
			path=$(pwd)
			echo -ne "Configuring stores and layers......"
			array=("risk1" "risk2" "risk3" "risk4" "risk5" "risk6" "risk7" "risk8" "risk9" "risk10" "risk11" "risk12" "risk_user")
			boundingBox='<nativeBoundingBox><minx>225370.7346</minx><maxx>774629.2654</maxx><miny>3849419.9580</miny><maxy>6914547.3835</maxy></nativeBoundingBox><latLonBoundingBox><minx>-6.0</minx><maxx>0.0</maxx><miny>34.75</miny><maxy>62.33</maxy><crs>EPSG:3042</crs></latLonBoundingBox>'
			echo -ne '\n###################      (70%)\n'
			sleep 1
			ite=70
			for i in ${!array[@]}; do
			  	# echo -ne " $i,${array[$i]} "
				curl -u $userGeoserver:$passGeoserver -XPOST -H "Content-Type: text/xml" -d "<coverageStore><name>"${array[$i]}"</name><workspace>signis_osgis</workspace><enabled>true</enabled><type>GeoTIFF</type><url>file:"$path"/"${array[$i]}".tif</url></coverageStore>" http://localhost:8080/geoserver/rest/workspaces/public/coveragestores > /dev/null;
				curl -u $userGeoserver:$passGeoserver -XPOST -H 'Content-type: text/xml' -d '<coverage><name>'${array[$i]}'</name><title>'${array[$i]}'</title><nativeCRS>GEOGCS[&quot;WGS 84&quot;,DATUM[&quot;World Geodetic System 1984&quot;,SPHEROID[&quot;WGS 84&quot;,6378137.0, 298.257223563, AUTHORITY[&quot;EPSG&quot;,&quot;7030&quot;]],AUTHORITY[&quot;EPSG&quot;,&quot;6326&quot;]],PRIMEM[&quot;Greenwich&quot;, 0.0, AUTHORITY[&quot;EPSG&quot;,&quot;8901&quot;]],UNIT[&quot;degree&quot;, 0.017453292519943295],AXIS[&quot;Geodetic longitude&quot;, EAST],AXIS[&quot;Geodetic latitude&quot;, NORTH],AUTHORITY[&quot;EPSG&quot;,&quot;4326&quot;]]</nativeCRS><srs>EPSG:3857</srs>'$latLonBoundingBox'<projectionPolicy>FORCE_DECLARED</projectionPolicy><dimensions><coverageDimension><name>GRAY_INDEX</name><description>GridSampleDimension[-Infinity,Infinity]</description><range><min>-inf</min><max>inf</max></range><nullValues><double>255.0</double></nullValues><dimensionType><name>UNSIGNED_8BITS</name></dimensionType></coverageDimension></dimensions></coverage>' http://localhost:8080/geoserver/rest/workspaces/$workspaceGeoserver/coveragestores/${array[$i]}/coverages > /dev/null;
				curl -u $userGeoserver:$passGeoserver -XPUT -H "Content-type: text/xml" -d "<layer><defaultStyle><name>model_style</name></defaultStyle></layer>" http://localhost:8080/geoserver/rest/layers/$workspaceGeoserver:${array[$i]} > /dev/null;
				((ite2=$ite+$i*2))
				echo -ne "###################      ($ite2%)\r"
				sleep 0.5
			done

			cd ../../../signis_osgis/signis
			echo -ne "Raster image published!";
			echo -ne '\n#######################  (94%)\n'
			sleep 1
			# gdal_translate ../reclass/siose.tif siose20190108T180000000Z.tif
			
			break;;
		[Nn]* ) break;;
		* ) echo -ne "Please answer yes or no.";;
	    esac
	done
	# Comment
	echo -ne 'Geoserver is configured...'
	echo -ne '\n######################## (95%)\n'
	sleep 0.5
	echo -ne "The last step is to configure a superuser to log in."
	# Comment
	# Create superuser
	while true; do
	    read -p "Do you wish to create a super user?" yn
	    case $yn in
		[Yy]* ) python manage.py createsuperuser; break;;
		[Nn]* ) break;;
		* ) echo -ne "Please answer yer or no.";;
	    esac
	done
	# Comment
	echo -ne "NICE!"
	echo -ne '\n#########################(100%)\n'
	sleep 0.5
	# Comment
	# Running server
	echo -ne "Running server..."
	python manage.py runserver
	break;;
    * ) echo -ne "Please answer 0 or 1.";;
  esac
done


