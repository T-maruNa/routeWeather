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
    __one_meter_lat = float(0.000277778) / 30
    # 1度 111kmなので111000で割って1m当たりの度数を取得
    __one_meter_lon = 1 / 111000
    __km_unit = 1000
    def __init__(self):
        super(getWeatherController, self).__init__()

    # 値が範囲内か判定する(内包表記のなかで書くと見にくかった)
    def getRangeCity(self ,lon, lat, t_lon, m_lon, t_lat, m_lat):
        _lon = float(lon)
        _lat = float(lat)
        return (t_lon > lon > m_lon ) and (t_lat > lat > m_lat)

    def getOpenWeatherMap(self, _city_id):
        result_data = []
        range_km = 10 * self.__km_unit
        diff_lon = range_km * self.__one_meter_lon
        diff_lat = range_km * self.__one_meter_lat
        cnt = 0
        # 市区町村の情報をgzipから取得
        with gzip.open(CITY_CODE_LIST, 'rb') as f:
            world_ctiys_data = json.load(f)

        japan_ctiys_data = [wcd for wcd in world_ctiys_data if wcd['country'] == 'JP']
        tager_city = [ocd for ocd in japan_ctiys_data if ocd['id'] == _city_id]
        # なぜか配列で取れない
        # base_lon = tager_city['coord']['lon']
        # base_lat = tager_city['coord']['lat']
        # ↑これでとれない なぜ？？？
        # 文字列で取得されるらしい
        # ↓これだと取れた
        base_lon = [lon['coord']['lon'] for lon in tager_city]
        base_lat = [lat['coord']['lat'] for lat in tager_city]

        # 指定の市の周りの範囲座標を設定
        top_lon = float(base_lon[0]) + diff_lon
        min_lon = float(base_lon[0]) - diff_lon
        top_lat = float(base_lat[0]) + diff_lat
        min_lat = float(base_lat[0]) - diff_lat
        around_ctiys_data = [acd for acd in japan_ctiys_data if self.getRangeCity(acd['coord']['lon'], acd['coord']['lat'], top_lon, min_lon, top_lat, min_lat)]
        # 各都市の温度、天気を取得する
        for ctiy in around_ctiys_data:
            id = ctiy['id']
            # APIのURLを得る
            url = self.__api.format(city_id=id, key=API_KEY)
            # 実際にAPIにリクエストを送信して結果を取得する
            r = requests.get(url)
            # 結果はJSON形式なのでデコード
            tmp = json.loads(r.text)
            if(tmp and tmp['cod'] == 200):
                result_data.append({
                     'name':tmp['name']
                    ,'weather':tmp['weather'][0]['description']
                    ,'temp':tmp['main']['temp'] // 10
                    ,'lon':ctiy['coord']['lon']
                    ,'lat':ctiy['coord']['lat']
                })
        
        return result_data
