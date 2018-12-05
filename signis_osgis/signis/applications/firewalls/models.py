# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.gis.db import models

# Create your models here.

class firewalls(models.Model):
    location = models.LineStringField(srid=3857)
    type = models.IntegerField()
    descript = models.CharField(max_length=70)