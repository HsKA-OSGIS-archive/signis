from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from applications.firewalls.views import index, testingQGIS

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^testing/', testingQGIS, name='testing'),
]
