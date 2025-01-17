# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys
import os
sys.path.insert(0, '../../model/code')
sys.path.insert(0, '../../model/model_data/meteo_data')

import test_model
import psycopg2
import psycopg2.extensions
import json
#from qgis.core import * 

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
"""from applications.firewalls.models import firewalls
from applications.firewalls.forms import FirewallsForm"""
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse


# Create your views here.
def model(request):
    if request.method == 'POST':
        m = request.POST['meteo']
        f = request.POST['firewalls']
        n_month = request.POST['month']
        print m, f, n_month
        ms = test_model.runModel(meteo=int(m),firewalls_input=int(f),m=int(n_month))
        print ms
        dicc ={}
        dicc['1'] = ms
        r = json.dumps(dicc)
        return HttpResponseRedirect("/viewer/")
    
if __name__== '__main__':
    test_model.runModel(0,1,7)
    
def uploadCSV_Valencia(request):
    doc_to_save = request.FILES['userV']
    #filename = doc_to_save._get_name()
    #filename = os.path.basename(filename)
    fd = open('../../model/model_data/meteo_data/' + str('userV.csv'), 'wb')
    for chunk in doc_to_save.chunks():
        fd.write(chunk)
    fd.close()
    return HttpResponseRedirect("/models/creating/")

def uploadCSV_Castellon(request):
    doc_to_save = request.FILES['userC']
    #filename = doc_to_save._get_name()
    #filename = os.path.basename(filename)
    fd = open('../../model/model_data/meteo_data/' + str('userC.csv'), 'wb')
    for chunk in doc_to_save.chunks():
        fd.write(chunk)
    fd.close()
    return HttpResponseRedirect("/models/creating/")

