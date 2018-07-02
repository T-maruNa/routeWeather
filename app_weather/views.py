from django.http.response import HttpResponse
from .controller import getWeatherController

def PassMethod():
    return HttpResponse('RouteWeather')

def weather(request):
    gw = getWeatherController()
    data = gw.getOpenWeatherMap(cities)
    return HttpResponse(data)
