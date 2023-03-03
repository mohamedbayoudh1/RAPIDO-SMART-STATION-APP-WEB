
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="stations"),
    path('add-station', views.add_station, name="add-station"),

]
 

