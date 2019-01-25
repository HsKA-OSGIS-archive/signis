from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from applications.models_firerisk.views import model

urlpatterns = [
    url(r'^new', login_required(model), name='model_new'),
]
