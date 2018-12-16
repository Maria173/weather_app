import sys
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow
from weather_yandex import Request


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('w_vidget.ui', self)
        self.pict.setPixmap(QPixmap('sun.jpg')) # Тут дефолтная картинка
        self.btn.clicked.connect(self.run)

    def run(self):
        self.value = self.citylist.currentText()
        if self.value != 'Выберите город':
            url = self.getSelectedCityUrl()
            self.rq = Request(url)
            self.rq.onSuccess(self.getCityWeather)

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
