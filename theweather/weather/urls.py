
from django.urls import path
from .views import index, city_detail, search

urlpatterns = [
    path('', index, name='index'),   
    path('find/', search, name='search'), 
    path('city/<int:geoname_id>', city_detail, name='city_detail'), 
]