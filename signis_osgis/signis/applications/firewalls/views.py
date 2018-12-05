# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from qgis.core import * 

from django.shortcuts import render
from django.http import HttpResponse
from applications.firewalls.models import firewalls
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

# Create your views here.
def index(request):
    return HttpResponse("Index")

class firewalls_select(ListView):
    model = firewalls
    #template_name = 'mascota/mascota_list.html'


class firewalls_insert(CreateView):
    model = firewalls
    #form_class = MascotaForm
    #template_name = 'mascota/mascota_form.html'
    #success_url = reverse_lazy('mascota:mascota_listar')


class firewalls_update(UpdateView):
    model = firewalls
    #form_class = MascotaForm
    #template_name = 'mascota/mascota_form.html'
    #success_url = reverse_lazy('mascota:mascota_listar')


class firewalls_delete(DeleteView):
    model = firewalls
    #template_name = 'mascota/mascota_delete.html'
    #success_url = reverse_lazy('mascota:mascota_listar')
    

def testingQGIS(request):
    return HttpResponse("testing")
