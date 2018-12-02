# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

from django.shortcuts import render

from django.http import HttpResponse
from django.contrib.auth.models import User
from applications.users.forms import RegistrationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy

# Create your views here.

class UserRegister(CreateView):
    model = User
    template_name = "users/register.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('index')
