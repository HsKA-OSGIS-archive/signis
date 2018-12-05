#!/bin/bash

# SERVER SIGNIS
echo "Starting..."
cd signis_osgis
# source bin/activate
# echo "Virtual environment"

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

cd signis
cd signis
# Conf app connection
while true; do
    read -p "Do you wish to configure the application connection?" yn
    case $yn in
        [Yy]* ) echo "Configuring application connection..."; 
		echo "This is only for development mode. Your user and password are in your local server. Commanly, the default user for postgres is postgres.";
		read -p "What's the postgres user: " namePostgres;
		read -sp "What's the postgres password: " passPostgres;
		read -p  "The default database name is 'signis_osgis'. Write the same name if the database is called like 'signis_osgis' or set another name for the database:" databasePostgres
		sed -i "82s/.*/        'NAME': '$databasePostgres',/" settings.py;
		sed -i "83s/.*/        'USER': '$namePostgres',/" settings.py;
		sed -i "84s/.*/        'PASSWORD': '$passPostgres',/" settings.py;
		echo "Application confidured for postgres user: $namePostgres"
		break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

# echo "Configuring application connection..."
# echo "This is only for development mode. Your user and password are in your local server. Commanly, the default user for postgres is postgres."
# echo "What's the postgres user:"
# read -p namePostgres
# echo "What's the postgres password:"
# read -sp passPostgres
# sed -i "81s/.*/        'NAME': 'SIGNIS',/" settings.py
# sed -i "82s/.*/        'USER': '$namePostgres',/" settings.py
# sed -i "83s/.*/        'PASSWORD': '$passPostgres',/" settings.py
# echo "Application confidured for postgres user: $namePostgres"

cd ..
# Migrate relations
echo "Migrating relations..."
while true; do
    read -p "Do you wish to migrate relations?" yn
    case $yn in
        [Yy]* ) python manage.py migrate; break;;
        [Nn]* ) break;;
        * ) echo "Please answer yes or no.";;
    esac
done

# Create superuser
echo "Super user..."
while true; do
    read -p "Do you wish to create a super user?" yn
    case $yn in
	[Yy]* ) python manage.py createsuperuser; break;;
	[Nn]* ) break;;
	* ) echo "Please answer yer or no.";;
    esac
done

# Running server
echo "Running server..."
python manage.py runserver

