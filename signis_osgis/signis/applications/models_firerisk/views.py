# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
sys.path.insert(0, '../../model/code')

import test_model
import psycopg2
import psycopg2.extensions
import json
#from qgis.core import * 

from django.shortcuts import render
from django.http import HttpResponse
"""from applications.firewalls.models import firewalls
from applications.firewalls.forms import FirewallsForm"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse


# Create your views here.
def model(request):
    if request.method == 'POST':
        m = request.POST['meteo']
        f = request.POST['firewalls']
        n_month = request.POST['month']
        ms = test_model.runModel(int(m),int(f),int(n_month))
        print 'Model created' + ms
        return render(request, 'templates/viewer.html')
    
if __name__== '__main__':
    test_model.runModel(0,1,7)