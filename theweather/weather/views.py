import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .models import City


# Create your views here.

# def home(request):
#     return HttpResponse("Project 3: TODO")


def index(request):
    api_key = os.environ['API_KEY']
    top_cities =["Vilnius", "Kaunas", "Klaipėda", "Šiauliai","Panevėžys"]
    cities = City.objects.filter(name__in = top_cities)
    weather_data = []
    for city in cities:
        id = city.geoname_id
        url = f'http://api.openweathermap.org/data/2.5/weather?id={id}&&units=metric&appid={api_key}'
        city_weather = requests.get(url).json() #request the API data and convert the JSON to Python data types
        weather = {
            'id' : city_weather['id'],
            'city' : city_weather['name'],
            'temperature' : round(city_weather['main']['temp'], 1),
            'feels_like' : round(city_weather['main']['feels_like'], 1),
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
       
    context = {
            'weather_data':weather_data
        }
    return render(request, 'index.html', context)

def city_detail(request, geoname_id):

    api_key = os.environ['API_KEY']
    cityObject = City.objects.get(geoname_id = geoname_id)


    # One Call API
    url = f'https://api.openweathermap.org/data/2.5/onecall?lat={cityObject.lat}&units=metric&lon={cityObject.lon}&exclude=minutely,hourly&appid={api_key}'
    city_weather = requests.get(url).json() #request the API data and convert the JSON to Python data types
    
    # current weather
    current_weather = {
            'sunrise' : city_weather['current']['sunrise'],
            'sunset' : city_weather['current']['sunset'],
            'temperature' : round(city_weather['current']['temp'], 1),
            'feels_like' : round(city_weather['current']['feels_like'], 1),
            'pressure' : city_weather['current']['pressure'],
            'humidity' : city_weather['current']['humidity'],
            'clouds' : city_weather['current']['clouds'],
            'uvi' : city_weather['current']['uvi'],
            'visibility' : city_weather['current']['visibility'],
            'wind_speed' : city_weather['current']['wind_speed'],
            'wind_deg' : city_weather['current']['wind_deg'],
            'main' : city_weather['current']['weather'][0]['main'],
            'description' : city_weather['current']['weather'][0]['description'],
            'icon' : city_weather['current']['weather'][0]['icon']
        }

    # forecast 8 days (current + 7days)
    forecast = []
    for day in city_weather['daily']:
        # print(round(day['temp']['morn'], 1))
        forecast_daily = {
            'sunrise' : day['sunrise'],
            'sunset' : day['sunset'],
            'temperature_morn' : round(day['temp']['morn'], 1),
            'temperature_day' : round(day['temp']['day'], 1),
            'temperature_eve' : round(day['temp']['eve'], 1),
            'temperature_night' : round(day['temp']['night'], 1),
            'temperature_min' : round(day['temp']['min'], 1),
            'temperature_max' : round(day['temp']['max'], 1),
            'feels_like_morn' : round(day['feels_like']['morn'], 1),
            'feels_like_day' : round(day['feels_like']['day'], 1),
            'feels_like_eve' : round(day['feels_like']['eve'], 1),
            'feels_like_night' : round(day['feels_like']['night'], 1),
            'pressure' : day['pressure'],
            'humidity' : day['humidity'],
            'clouds' : day['clouds'],
            'uvi' : day['uvi'],
            'wind_speed' : day['wind_speed'],
            'wind_deg' : day['wind_deg'],
            'main' : day['weather'][0]['main'],
            'description' : day['weather'][0]['description'],
            'icon' : day['weather'][0]['icon']
        }
        forecast.append(forecast_daily)

    context = {
            'current_weather':current_weather,
            'forecast':forecast,
        }
    return render(request, 'city.html', context)

def search(request):
    api_key = os.environ['API_KEY']
    cityName = request.GET.get('cityName')
    cityObject = City.objects.get(name = cityName)

    # get current weather
    url= f'http://api.openweathermap.org/data/2.5/weather?id={cityObject.geoname_id}&&units=metric&appid={api_key}'
    city_weather = requests.get(url).json() #request the API data and convert the JSON to Python data types
    weather = {
        'id' : city_weather['id'],
        'city' : city_weather['name'],
        'temperature' : round(city_weather['main']['temp'], 1),
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }

    context = {
            'weather':weather
        }
    return render(request, 'searchresults.html', context)
