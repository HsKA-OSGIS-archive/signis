"""Users URL Configuration"""
from django.conf.urls import url
from applications.users.views import UserRegister

urlpatterns = [
    url(r'register', UserRegister.as_view(), name='registration')
]
