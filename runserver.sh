#!/bin/bash

# SERVER SIGNIS
echo "Starting..."
cd signis_ogis
source bin/activate
echo "Virtual environment"

cd signis

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

