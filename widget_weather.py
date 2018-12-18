import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow
from weather_yandex import Request


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('w_vidget.ui', self)
        self.dict_conditions = {'тепло': 'sun.png', 'прохладно': 'clouds.png',
                                'дождь': 'rain.png', 'ливень': 'rain.png',
                                'снег': 'snow.png', 'гроза': 'thunder.png',
                                'ok': 'def.png'}
        self.image_profile = QImage('default.jpg')
        self.image_profile = self.image_profile.scaled(200, 00,
        aspectRatioMode=QtCore.Qt.KeepAspectRatio,
        transformMode=QtCore.Qt.SmoothTransformation)r
        self.pict.setPixmap(QPixmap.fromImage(self.image_profile))
        self.show()
        self.btn.clicked.connect(self.run)

    def run(self):
        self.value = self.citylist.currentText()
        if self.value != 'Выберите город':
            url = self.getSelectedCityUrl()
            self.rq = Request(url)
            self.rq.onSuccess(self.getCityWeather)

        else:
            self.main_text.setText('Пожалуйста, укажите \nгород.')

    def getSelectedCityUrl(self):
        return 'http://dataservice.accuweather.com/locations/v1/cities/search?apikey=2wAZfZ1bYGOAIK6xmWXUBnAxVHwt952H&q={}'.format(self.value)

    def getWeatherUrl(self):
        key = self.rq.getKey()
        return "http://dataservice.accuweather.com/currentconditions/v1/{}.json?language=ru-ru&details=true&apikey=2wAZfZ1bYGOAIK6xmWXUBnAxVHwt952H".format(key)

    def getCityWeather(self):
        url = self.getWeatherUrl()
        self.req = Request(url)
        self.req.onSuccess(self.req.generateText)
        self.req.onSuccess(self.showTemp)
        self.req.onSuccess(self.showDateTime)
        self.req.onSuccess(self.showWhatToWear)
        self.req.onSuccess(self.change_Image)

    def change_Image(self):

        self.image_profile = QImage(self.dict_conditions[self.req.getConditions()])
        self.image_profile = self.image_profile.scaled(200, 200,
                                                       aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                       transformMode=QtCore.Qt.SmoothTransformation)
        self.pict.setPixmap(QPixmap.fromImage(self.image_profile))
        self.repaint()


    def showTemp(self):
        self.temperature.setText(str(self.req.getTemp()))

    def showDateTime(self):
        self.date_time.setText(str(self.req.getDateTime()))

    def showWhatToWear(self):
        self.main_text.setText(str(self.req.what_to_wear()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
