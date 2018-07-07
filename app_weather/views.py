from django.http.response import HttpResponse
from .controller import getWeatherController
from django.http.response import JsonResponse


def PassMethod():
    return HttpResponse('RouteWeather')

def weather(request):
    gw = getWeatherController()
    # 仮値で伊勢崎のID
    city_id = 1861436
    data = gw.getOpenWeatherMap(city_id)
    return HttpResponse(data)
