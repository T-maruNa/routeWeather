import requests
import json
import gzip

from .config import API_KEY, CITY_CODE_LIST

class getWeatherController:
    """docstring for getWeather."""
    #api URL keyを設定
    __api = "http://api.openweathermap.org/data/2.5/weather?id={city_id}&APPID={key}"

    def __init__(self):
        super(getWeatherController, self).__init__()

    def getOpenWeatherMap(self, cities):
        result_data = []

        # 市区町村の情報をgzipから取得
        with gzip.open(CITY_CODE_LIST,'rb',9) as f:
            world_ctiys_data = json.load(f)
            japan_ctiys_data = [wcd for wcd in world_ctiys_data if wcd['country'] == 'JP']

        cnt = 0
        # 各都市の温度を取得する
        for ctiy in japan_ctiys_data:
            # あっちゅーまにAPIのリクエスト限界が来てしまうのでリミット設定
            cnt+=1
            if cnt == 5 :
                return data

            id = ctiy['id']
            # APIのURLを得る
            url = self.__api.format(city_id=id, key=API_KEY)
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
        return result_data
