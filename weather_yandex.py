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
        self.date_time = Date + '\n' + Time

        def compare_temp(self, t):
            if t < -30.0:
                return 'пуховик или шубу; приветствуется многослойность.'
            elif (t >= -30.0) and (t < -20.0):
                return 'куртку на синтепоне или дублёнку.'
            elif (t >= -20.0) and (t < -10.0):
                return 'шерстяное пальто или шубу из искусственного меха.'
            elif (t >= -10.0) and (t < 0.0):
                return 'пальто или куртку.'
            elif (t >= 0.0) and (t < 10.0):
                return 'теплый плащ или лёгкое пальто.'
            elif (t >= 10.0) and (t < 20.0):
                return 'ветровку или джинсовую куртку.'
            elif (t >= 20.0) and (t < 30.0):
                return 'что-нибудь лёгкое из хлопка или смесовых тканей.'
            elif t >= 30.0:
                return 'что-нибудь лёгкое из натуральных тканей (лен, хлопок, шелк и т.д.).'

        def compare_humidity(self, humidity):
            if (humidity >= 0) and (humidity <= 33):
                return 'пару бутылочек с водой и влажные салфетки :)'
            elif (humidity > 33) and (humidity <= 66):
                return 'бутылочку с водой и пачку бумажных салфеток :)'
            elif (humidity > 66) and (humidity <= 100):
                return 'пачку бумажныых салфеток :)'

        def compare_conditions(self, text):
            if 'солнечно' in text or 'ясно' in text:
                return 'солнечные очки.'
            elif 'облачно' in text or 'пасмурно' in text or 'ветренно' in text or 'ветер' in text:
                return 'шарф и головной убор.'
            elif 'дождь' in text:
                return 'зонт и резиновые сапоги.'
            elif 'ливень' in text:
                return 'дождевик и резиновые сапоги.'
            elif 'снег' in text or 'лёд' in text or 'лед' in text:
                return 'высокие сапоги и тёплый головной убор.'
            elif 'гроза' in text or 'гром' in text or 'гром' in text:
                return 'возможность взять такси (на улице гроза, и я очень волнуюсь за тебя)!'
            else:
                return 'хорошее настроение и наслаждаться погодой!'

        self.generation_by_temp = 'Из одежды рекомендую тебе выбрать ' + compare_temp(self, self.temp)
        self.generation_by_humidity = 'Советую не забыть про ' + compare_humidity(self, self.humidity)
        self.generation_by_text = 'Думаю, будет не лишним захватить с собой ' + \
                                  compare_conditions(self, self.weather_text)

    def getConditions(self):
        return self.generation_by_text

    def getTemp(self):
        return str(self.temp) + '°C'

    def getDateTime(self):
        return self.date_time

    def what_to_wear(self):
        return self.generation_by_temp + ' ' + self.generation_by_text + ' ' + self.generation_by_humidity

    def onSuccess(self, callback):
        self.callbacks.append(callback)
