import requests
import json
from .config import api_key

# 天気を調べたい都市の一覧
#cities = ["Tokyo,JP", "London,UK", "New York,US"]

class getWeatherController:
    """docstring for getWeather."""
    #api URL keyを設定
    __api = "http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
    __apikey = api_key
    __cities = [];
    def __init__(self, cities):
        super(getWeatherController, self).__init__()
        self.__cities = cities

    def getOpenWeatherMap(self):
        data = []

        # 各都市の温度を取得する
        for name in self.__cities:
            tmp = ''
            # APIのURLを得る
            url = self.__api.format(city=name, key=self.__apikey)
            # 実際にAPIにリクエストを送信して結果を取得する
            r = requests.get(url)
            # 結果はJSON形式なのでデコード
            tmp = json.loads(r.text)
            if(tmp and tmp['cod'] == 200):
                data.append([
                     tmp['name']
                    ,tmp['weather'][0]['description']
                    ,tmp['main']['temp'] // 10
                ])
        return data

cities = ["Tokyo,JP", "Saitama,JP"]
a = getWeatherController(cities)
a.getOpenWeatherMap()
