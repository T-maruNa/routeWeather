from django.http.response import HttpResponse
from .controller import getWeatherController

def PassMethod():
    return HttpResponse('RouteWeather')

def weather(request):
    gw = getWeatherController()
    # 仮値で伊勢崎のID
    cities = 1861436
    data = gw.getOpenWeatherMap(cities)
    return HttpResponse(data)
