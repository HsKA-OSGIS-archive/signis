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


