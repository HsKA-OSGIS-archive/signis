# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from applications.firewalls.models import firewalls
from django.contrib.gis import admin

# Register your models here.
admin.site.register(firewalls, admin.OSMGeoAdmin)
