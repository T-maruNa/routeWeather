import requests
import json
import gzip

from .config import API_KEY, CITY_CODE_LIST

class getWeatherController:
    """docstring for getWeather."""
    #api URL keyを設定
    __api = "http://api.openweathermap.org/data/2.5/weather?id={city_id}&APPID={key}"
    # 0.000277778 は30m当たりの度数なので30で割ることで1m当たりの度数を取得
    # 詳しくはwebで
    __one_meter = 0.000277778 / 30

    def __init__(self):
        super(getWeatherController, self).__init__()

    def getOpenWeatherMap(self, cities):
        result_data = []
        diff_point_lon = 50 * 1000 * self.__one_meter

        # 市区町村の情報をgzipから取得
        with gzip.open(CITY_CODE_LIST,'rb',9) as f:
            world_ctiys_data = json.load(f)
            japan_ctiys_data = [wcd for wcd in world_ctiys_data if wcd['country'] == 'JP']

        #only_ctiy_data = [[ocd['name'],ocd['coord']['lon']] for ocd in japan_ctiys_data if ocd['id'] == cities]
        only_ctiy_data = [ocd for ocd in japan_ctiys_data if ocd['id'] == cities]
        return only_ctiy_data
        #base_lon =
        top_point_lon = base_lon + diff_point_lon
        min_point_lon = base_lon - diff_point_lon
        around_ctiys_data = [acd for acd in japan_ctiys_data if top_point_lon > japan_ctiys_data['coord']['lon'] > min_point_lon]

        # 各都市の温度を取得する
        # あっちゅーまにAPIのリクエスト限界が来てしまうのでリミット設定
        for ctiy in around_ctiys_data[0:5]:
            id = ctiy['id']
            # APIのURLを得る
            url = self.__api.format(city_id=id, key=API_KEY)
            # 実際にAPIにリクエストを送信して結果を取得する
            r = requests.get(url)
            # 結果はJSON形式なのでデコード
            tmp = json.loads(r.text)
            if(tmp and tmp['cod'] == 200):
                result_data.append([
                     tmp['name']
                    ,tmp['weather'][0]['description']
                    ,tmp['main']['temp'] // 10
                    ,ctiy
                ])
        return result_data
