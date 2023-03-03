from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="tanks"),
    path('add-tank', views.add_tank, name="add-tanks"),
    path('edit-tank/<int:id>', views.tank_edit, name="tank-edit"),
    path('tank-delete/<int:id>', views.delete_tank, name="tank-delete"),
    path('search-tanks', csrf_exempt(views.search_tanks),
         name="search_tanks"),
    path('tank_category_summary', views.tank_category_summary,
         name="tank_category_summary"),
    path('stats', views.stats_view,
         name="stats")
]