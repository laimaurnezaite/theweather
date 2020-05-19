import os
from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import City


# Create your views here.

# def home(request):
#     return HttpResponse("Project 3: TODO")


def index(request):
    api_key = os.environ['API_KEY']
    cities = City.objects.all()
    weather_data = []
    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&&units=metric&appid={api_key}'
        city_weather = requests.get(url).json() #request the API data and convert the JSON to Python data types
        weather = {
            'city' : city.name,
            'temperature' : round(city_weather['main']['temp'], 1),
            'feels_like' : round(city_weather['main']['feels_like'], 1),
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
       

    # print(cities)
    # city = 'Vilnius'
    # url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&&units=metric&appid={api_key}'
    # city_weather = requests.get(url).json() #request the API data and convert the JSON to Python data types
    # print("TEST2")
    # print(city_weather)
    # weather = {
    #     'city' : city,
    #     'temperature' : city_weather['main']['temp'],
    #     'feels_like' : city_weather['main']['feels_like'],
    #     'description' : city_weather['weather'][0]['description'],
    #     'icon' : city_weather['weather'][0]['icon']
    # }
    context = {
            'weather_data':weather_data
        }
    return render(request, 'index.html', context)