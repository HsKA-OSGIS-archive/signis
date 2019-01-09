# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import psycopg2
import psycopg2.extensions
import json
#from qgis.core import * 

from django.shortcuts import render
from django.http import HttpResponse
from applications.firewalls.models import firewalls
from applications.firewalls.forms import FirewallsForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse

# Create your views here.
def firewalls_insert(request):
    if request.method == 'POST':
        geom = request.POST['geom']
        type = request.POST['type']
        descript = request.POST['descript']
        
        # Connect to the database
        conn = psycopg2.connect(database='signis', user='', password='', host='localhost', port='5432')
        cursor = conn.cursor()
        d_conn = {}
        d_conn['conn'] = conn
        d_conn['cursor'] = cursor
        conn = d_conn['conn']
        cursor = d_conn['cursor']
        
        # Obtain data
        d_form_data = {}
        d_form_data['geom'] = geom
        d_form_data['type'] = type
        d_form_data['descript'] = descript
        d_form_data['geom'] = transform_coords_ol_to_postgis(coords_geom=d_form_data['geom'])
        d2 = dict_to_string_fields_and_vector_values2(d=d_form_data)
        str_field_names = d2['str_field_names']
        list_field_values = d2['list_field_values']
        str_s_values = d2['str_s_values']
        
        # Insert sentence
        cons_ins = 'insert into {0} ({1}) values ({2})'.format('firewalls_firewalls', str_field_names, str_s_values)
        
        # Execute
        cursor.execute(cons_ins,list_field_values)
        conn.commit()
        return HttpResponse("Firewall Inserted")
    
def firewalls_update(request):
    if request.method == 'POST':
        id = request.POST['id']
        geom = request.POST['geom']
        type = request.POST['type']
        descript = request.POST['descript']
        
        # Connect to the database
        conn = psycopg2.connect(database='signis', user='', password='', host='localhost', port='5432')
        cursor = conn.cursor()
        d_conn = {}
        d_conn['conn'] = conn
        d_conn['cursor'] = cursor
        conn = d_conn['conn']
        cursor = d_conn['cursor']
        
        # Obtain data
        d_form_data = {}
        d_form_data['geom'] = geom
        d_form_data['type'] = type
        d_form_data['descript'] = descript
        d_form_data['geom'] = transform_coords_ol_to_postgis(coords_geom=d_form_data['geom'])
        d2 = dict_to_string_fields_and_vector_values2(d=d_form_data)
        str_field_names = d2['str_field_names']
        list_field_values = d2['list_field_values']
        str_s_values = d2['str_s_values']
        cond_where = 'where id = %s' 
        list_values_cond_where = [id]
        
        # Insert sentence
        cons_up = 'update {table_name} set ({str_field_names}) = ({str_s_values})'.format(table_name='firewalls_firewalls', str_field_names=str_field_names, str_s_values=str_s_values)
        
        # Execute
        cons_up += ' ' + cond_where
        cursor.execute(cons_up,list_field_values + list_values_cond_where)
        conn.commit()
        return HttpResponse("Firewall Updated")
    
def firewalls_delete(request):
    if request.method == 'POST':
        id = request.POST['id']
        
        # Connect to the database
        conn = psycopg2.connect(database='signis', user='', password='', host='localhost', port='5432')
        cursor = conn.cursor()
        d_conn = {}
        d_conn['conn'] = conn
        d_conn['cursor'] = cursor
        conn = d_conn['conn']
        cursor = d_conn['cursor']
        
        # Obtain data
        cond_where = 'where id = %s' 
        list_values_cond_where = [id]
        
        # Insert sentence
        cons_del = cons='delete from {table_name}'.format(table_name='firewalls_firewalls')
        
        # Execute
        cons_del += ' ' + cond_where
        cursor.execute(cons_del, list_values_cond_where)
        conn.commit()
        return HttpResponse("Firewall Deleted")
      
def transform_coords_ol_to_postgis(coords_geom, splitString=','):
    lc=coords_geom.split(splitString)
    n=len(lc)
    sc=''
    for i in xrange(0,n,2):
        x=lc[i]
        y=lc[i+1]
        sc=sc + ',' + x + ' ' + y
    return sc[1:]  

def dict_to_string_fields_and_vector_values2(d,list_fields_to_remove=None, geom_field_name='geom', epsg='3857', geometry_type='MULTILINESTRING', epsg_to_reproject=None):
    #remove the fileds to delete
    if list_fields_to_remove <> None:
        for i in range(len(list_fields_to_remove)):
            key=list_fields_to_remove[i]
            del d[key]
    
    #adds the geometry type and the paranthesis to the coordinates
    coords=d.get(geom_field_name,'')
    geometry_type=geometry_type.upper()
    if coords<>'':#hay geometrÃ­a
        if geometry_type=='POLYGON':
            coords='POLYGON(({coords}))'.format(coords=coords)
        elif geometry_type=='LINESTRING':
            coords='LINESTRING({coords})'.format(coords=coords)
        elif geometry_type=='POINT':
            coords='POINT({coords})'.format(coords=coords)
        elif geometry_type=='MULTIPOLYGON':
            coords='MULTIPOLYGON((({coords})))'.format(coords=coords)
        elif geometry_type=='MULTILINESTRING':
            coords='MULTILINESTRING(({coords}))'.format(coords=coords)
        elif geometry_type=='MULTIPOINT':
            coords='MULTIPOINT(({coords}))'.format(coords=coords)
        d[geom_field_name]=coords
    
    #forms the tree values returned in the dictionary
    it=d.items()
    str_name_fields=''
    list_values =[]     
    str_s_values=''
    for i in range(len(it)):
        str_name_fields = str_name_fields + it[i][0] + ','
        #change the '' values by None
        if it[i][1]=='':
            list_values.append(None) 
        else:
            list_values.append(it[i][1])  
            
        if it[i][0] <> geom_field_name:
            str_s_values=str_s_values + '%s,'
        else:
            if epsg_to_reproject is None:
                st='st_geometryfromtext(%s,{epsg}),'.format(epsg=epsg)
                str_s_values=str_s_values + st
            else:
                st='st_transform(st_geometryfromtext(%s,{epsg}),{epsg_to_reproject}),'.format(epsg=epsg, epsg_to_reproject=epsg_to_reproject)
                str_s_values=str_s_values + st             
            #(%s,st_geometryfromtext(%s,25830))           
    str_name_fields=str_name_fields[:-1]
    str_s_values=str_s_values[:-1]
    df={}
    df['str_field_names']=str_name_fields
    df['list_field_values']=list_values
    df['str_s_values']=str_s_values
    return df

