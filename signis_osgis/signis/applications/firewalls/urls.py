from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from applications.firewalls.views import firewalls_insert, firewalls_update, firewalls_delete

urlpatterns = [
    url(r'^new', login_required(firewalls_insert), name='firewall_new'),
    url(r'^update', login_required(firewalls_update), name='firewall_update'),
    url(r'^delete', login_required(firewalls_delete), name='firewall_delete'),
]
