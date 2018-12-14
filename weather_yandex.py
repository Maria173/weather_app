import sys
from PyQt5 import QtNetwork
from PyQt5.QtCore import QUrl, QCoreApplication
import json


class Example:

    def __init__(self):

        self.doRequest()

    def doRequest(self):

        url = "http://dataservice.accuweather.com/currentconditions/v1/296217.json?language=ru-ru&details=true&apikey=2wAZfZ1bYGOAIK6xmWXUBnAxVHwt952H"
        req = QtNetwork.QNetworkRequest(QUrl(url))

        self.nam = QtNetwork.QNetworkAccessManager()
        self.nam.finished.connect(self.handleResponse)
        self.nam.get(req)

    def handleResponse(self, reply):

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:

            bytes_string = reply.readAll()
            resp_str = str(bytes_string, 'utf-8')
            print("RESPONSE:" + resp_str)
            # self.temp = str(resp_obj[0]['RealFeelTemperature']['Metric']['Value']) + resp_obj[0]['RealFeelTemperature']['Metric']['Unit']
            resp_obj = json.loads(resp_str)
            LocalObservationDateTime = resp_obj[0]['LocalObservationDateTime']

            self.weather_text = resp_obj[0]['WeatherText'].lower()
            self.temp = resp_obj[0]['Temperature']['Metric']['Value']
            self.humidity = resp_obj[0]['RelativeHumidity']
            LocalObservationDate = LocalObservationDateTime[:10]
            LocalObservationTime = LocalObservationDateTime[11:19]

            def compare_temp(self, temp):
                if temp < -30.0:
                    return 'очень холодно'
                elif (temp >= -30.0) and (temp < -20.0):
                    return 'морозно'
                elif (temp >= -20.0) and (temp < -10.0):
                    return 'холодно'
                elif (temp >= -10.0) and (temp < 0.0):
                    return 'прохладно'
                elif (temp >= 0.0) and (temp < -0.0):
                    return 'нормально'
                elif (temp >= 10.0) and (temp < 20.0):
                    return 'тепло'
                elif (temp >= 20.0) and (temp < 30.0):
                    return 'жарко'
                elif temp >= 30.0:
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

            print(compare_temp(self, self.temp))
            print(compare_humidity(self, self.humidity))
            print(compare_conditions(self, self.weather_text))


        else:
            print("Error occured: ", er)
            print(reply.errorString())

    # def getWeather(self):
    #     return resp_obj[0]['RealFeelTemperature']['Value']


if __name__ == '__main__':
    app = QCoreApplication([])
    ex = Example()
    QCoreApplication.quit()
    sys.exit(app.exec_())
