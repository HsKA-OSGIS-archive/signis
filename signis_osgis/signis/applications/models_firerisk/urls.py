from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

from applications.models_firerisk.views import model, uploadCSV

urlpatterns = [
    url(r'^new', login_required(model), name='model_new'),
    url(r'^upload/', login_required(uploadCSV), name='uploadCSV'),
]
