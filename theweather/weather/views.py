import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests
from .models import City
from datetime import datetime
# import datetime
# from dateutil import tz
# import datetime


# Create your views here.

# def home(request):
#     return HttpResponse("Project 3: TODO")


def index(request):
    api_key = os.environ['API_KEY']
    top_cities =[593116, 598316, 598098, 594739,596128]
    cities = City.objects.filter(geoname_id__in = top_cities)
    weather_data = []
    for city in cities:
        id = city.geoname_id
        url = f'http://api.openweathermap.org/data/2.5/weather?id={id}&&units=metric&appid={api_key}'
        city_weather = requests.get(url).json() #request the API data and convert the JSON to Python data types
        weather = {
            'id' : city_weather['id'],
            'city' : city.name,
            'temperature' : round(city_weather['main']['temp']),
            'feels_like' : round(city_weather['main']['feels_like']),
            'description' : city_weather['weather'][0]['description'],
            'icon' : f'http://openweathermap.org/img/wn/{city_weather["weather"][0]["icon"]}.png',
            # 'icon' : city_weather['weather'][0]['icon']
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
            'date' : datetime.utcfromtimestamp(city_weather['current']['dt']).strftime('%Y %m %d'),
            'name' : cityObject.name,
            'sunrise' : city_weather['current']['sunrise'],
            'sunset' : city_weather['current']['sunset'],
            'temperature' : round(city_weather['current']['temp']),
            'feels_like' : round(city_weather['current']['feels_like']),
            'pressure' : city_weather['current']['pressure'],
            'humidity' : city_weather['current']['humidity'],
            'clouds' : city_weather['current']['clouds'],
            'uvi' : city_weather['current']['uvi'],
            'visibility' : city_weather['current']['visibility'],
            'wind_speed' : city_weather['current']['wind_speed'],
            'wind_deg' : city_weather['current']['wind_deg'],
            'main' : city_weather['current']['weather'][0]['main'],
            'description' : city_weather['current']['weather'][0]['description'],
            'icon' : f'http://openweathermap.org/img/wn/{ city_weather["current"]["weather"][0]["icon"] }.png',
            # 'icon' : city_weather['current']['weather'][0]['icon']
        }

    # forecast 8 days (current + 7days)
    forecast = []
    for day in city_weather['daily']:
 
        forecast_daily = {
            # 'date': datetime.utcfromtimestamp(day['dt']).strftime('%Y %m %d'),
            'date_day': datetime.utcfromtimestamp(day['dt']).strftime('%Y %m %d'),
            'week_day': datetime.utcfromtimestamp(day['dt']).strftime('%A'),
            'sunrise': datetime.utcfromtimestamp(day['sunrise']).strftime('%H:%M'),
            'sunset' : datetime.utcfromtimestamp(day['sunset']).strftime('%H:%M'),
            # 'sunrise' : day['sunrise'],
            # 'sunset' : day['sunset'],
            'temperature_morn' : round(day['temp']['morn']),
            'temperature_day' : round(day['temp']['day']),
            'temperature_eve' : round(day['temp']['eve']),
            'temperature_night' : round(day['temp']['night']),
            'temperature_min' : round(day['temp']['min']),
            'temperature_max' : round(day['temp']['max']),
            'feels_like_morn' : round(day['feels_like']['morn']),
            'feels_like_day' : round(day['feels_like']['day']),
            'feels_like_eve' : round(day['feels_like']['eve']),
            'feels_like_night' : round(day['feels_like']['night']),
            'pressure' : day['pressure'],
            'humidity' : day['humidity'],
            'clouds' : day['clouds'],
            'uvi' : day['uvi'],
            'wind_speed' : day['wind_speed'],
            'wind_deg' : day['wind_deg'],
            'main' : day['weather'][0]['main'],
            'description' : day['weather'][0]['description'],
            'icon' : f'http://openweathermap.org/img/wn/{ day["weather"][0]["icon"] }@2x.png',
            # 'icon' : day['weather'][0]['icon']
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
    cityObject = City.objects.filter(name = cityName)
    weather_data = []
    for city in cityObject:
        
        id = city.geoname_id
        url = f'http://api.openweathermap.org/data/2.5/weather?id={id}&&units=metric&appid={api_key}'
        city_weather = requests.get(url).json() #request the API data and convert the JSON to Python data types
        weather = {
            'id' : city_weather['id'],
            'city' : city.name,
            'lat' : city.lat,
            'lon' : city.lon,
            'country':city.country,
            'temperature' : round(city_weather['main']['temp']),
            'feels_like' : round(city_weather['main']['feels_like']),
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
    if len(weather_data) == 0:
        context = {
            'message':"Sorry, no cities found in search"
        }
        return render(request, 'apology.html', context)

    context = {
            'weather_data':weather_data
        }
    return render(request, 'searchresults.html', context)



    # get current weather
    url= f'http://api.openweathermap.org/data/2.5/weather?id={cityObject.geoname_id}&&units=metric&appid={api_key}'
    city_weather = requests.get(url).json() #request the API data and convert the JSON to Python data types
    weather = {
        'id' : city_weather['id'],
        'city' : city_weather['name'],
        'temperature' : round(city_weather['main']['temp']),
        'description' : city_weather['weather'][0]['description'],
        'icon' : city_weather['weather'][0]['icon']
    }

    context = {
            'weather':weather
        }
    return render(request, 'searchresults.html', context)
