from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from applications.firewalls.views import firewalls_insert

urlpatterns = [
    url(r'^new$', login_required(firewalls_insert.as_view()), name='firewall_new'),
    #url(r'^update/(?P<pk>\d+)/$', login_required(CustomerUpdate.as_view()), name='customer_update'),

]
