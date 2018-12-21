import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow
from weather_yandex import Request
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('w_vidget.ui', self)
        intro = 'Думаю, будет не лишним захватить с собой '
        self.dict_conditions = {intro + 'солнечные очки.': 'sun.png',
                                intro + 'шарф и головной убор.': 'clouds.png',
                                intro + 'зонт и резиновые сапоги.': 'rain.png',
                                intro + 'дождевик и резиновые сапоги.': 'rain.png',
                                intro + 'высокие сапоги и тёплый головной убор.': 'snow.png',
                                intro + 'возможность взять такси (на улице гроза, и я очень волнуюсь за тебя)!':
                                    'thunder.png',
                                intro + 'хорошее настроение и наслаждаться погодой!': 'def.png'}
        self.image_profile = QImage('kevin.png')
        self.main_text.setText('Привет! Меня зовут Кевин :)\nХочешь узнать погоду? Тогда укажи город,\nв котором находишься!')
        self.main_text.setAlignment(Qt.AlignCenter)
        self.image_profile = self.image_profile.scaled(200, 200,
        aspectRatioMode=QtCore.Qt.KeepAspectRatio,
        transformMode=QtCore.Qt.SmoothTransformation)
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
            self.main_text.setText('Пожалуйста, укажи город :)')


    def getSelectedCityUrl(self):
        return 'http://dataservice.accuweather.com/locations/v1/cities/search?' \
               'apikey=icFNU4x13nHy5dJy0mIdXIAYi0E8TJF8&q={}'.format(self.value)

    def getWeatherUrl(self):
        key = self.rq.getKey()
        return "http://dataservice.accuweather.com/currentconditions/v1/{}.json?" \
               "language=ru-ru&details=true&apikey=icFNU4x13nHy5dJy0mIdXIAYi0E8TJF8".format(key)

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
        self.main_text.setWordWrap(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec())
