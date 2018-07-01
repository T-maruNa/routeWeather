from django.http.response import HttpResponse
from .controller import getWeatherController

def PassMethod():
    return HttpResponse('RouteWeather')

def weather(request):
    cities = ["Tokyo,JP", "Gunma,JP"]
    gw = getWeatherController(cities)
    data = gw.getOpenWeatherMap()
    return HttpResponse(data)
