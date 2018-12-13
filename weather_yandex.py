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
            print("RESP OBJ:")
            print(resp_obj[0]['WeatherText'])

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
