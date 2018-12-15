from PyQt5 import QtNetwork
from PyQt5.QtCore import QUrl
import json


class Request:

    def __init__(self, url):
        self.url = url
        # self.doRequestCity()
        self.doRequest()
        self.callbacks = []

    def doRequest(self):
        req = QtNetwork.QNetworkRequest(QUrl(self.url))

        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)

    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()
            resp_str = str(bytes_string, 'utf-8')
            self.resp_obj = json.loads(resp_str)

            for cb in self.callbacks:
                cb()

        else:
            print("Error occured: ", er)
            print(reply.errorString())
            bytes_string = reply.readAll()
            resp_str = str(bytes_string, 'utf-8')
            self.resp_obj = json.loads(resp_str)
            print ('[DEBUG] ' + self.resp_obj['Message'])

    def getKey(self):
        return self.resp_obj[0]['Key']

    def generateText(self):
        LocalObservationDateTime = self.resp_obj[0]['LocalObservationDateTime']
        self.weather_text = self.resp_obj[0]['WeatherText'].lower()
        self.temp = self.resp_obj[0]['Temperature']['Metric']['Value']
        self.humidity = self.resp_obj[0]['RelativeHumidity']
        Date = LocalObservationDateTime[:10]
        Time = LocalObservationDateTime[11:19]
        self.date_time = Date + ' ' + Time

        def compare_temp(self, t):
            if t < -30.0:
                return 'очень холодно'
            elif (t >= -30.0) and (t < -20.0):
                return 'морозно'
            elif (t >= -20.0) and (t < -10.0):
                return 'холодно'
            elif (t >= -10.0) and (t < 0.0):
                return 'прохладно'
            elif (t >= 0.0) and (t < -0.0):
                return 'нормально'
            elif (t >= 10.0) and (t < 20.0):
                return 'тепло'
            elif (t >= 20.0) and (t < 30.0):
                return 'жарко'
            elif t >= 30.0:
                return 'очень жарко'

        def compare_humidity(self, humidity):
            if humidity == 0:
                return '0%'
            elif (humidity > 0) and (humidity <= 33):
                return '20%'
            elif (humidity > 33) and (humidity <= 66):
                return '50%'
            elif (humidity > 66) and (humidity <= 100):
                return '80%'

        def compare_conditions(self, text):
            if 'солнечно' in text or 'ясно' in text:
                return 'тепло'
            elif 'облачно' in text or 'пасмурно' in text or 'ветренно' in text or 'ветер' in text:
                return 'прохладно'
            elif 'дождь' in text:
                return 'дождь'
            elif 'ливень' in text:
                return 'ливень'
            elif 'снег' in text or 'лёд' in text or 'лед' in text:
                return 'снег'
            elif 'гроза' in text or 'гром' in text or 'гром' in text:
                return 'гроза'
            else:
                return 'ok'

        self.generation_by_temp = compare_temp(self, self.temp)
        self.generation_by_humidity = compare_humidity(self, self.humidity)
        self.generation_by_text = compare_conditions(self, self.weather_text)

    def getTemp(self):
        return self.temp

    def getDateTime(self):
        return self.date_time

    def what_to_wear(self):
        return self.generation_by_temp + ' ' + self.generation_by_humidity + ' ' + self.generation_by_text

    def onSuccess(self, callback):
        self.callbacks.append(callback)

