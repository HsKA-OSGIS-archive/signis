from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from applications.models_firerisk.views import model, uploadCSV_Valencia, uploadCSV_Castellon

urlpatterns = [
    url(r'^new', login_required(model), name='model_new'),
    url(r'^uploadV/', login_required(uploadCSV_Valencia), name='uploadCSV_Valencia'),
    url(r'^uploadC/', login_required(uploadCSV_Castellon), name='uploadCSV_Castellon'),
]
