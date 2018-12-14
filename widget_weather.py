import sys
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('w_vidget.ui', self)
        self.pict.setPixmap(QPixmap('sun.jpg')) # Тут дефолтная картинка
        self.btn.clicked.connect(self.run)

    def run(self):
        self.value = self.citylist.currentText()
        if self.value == 'Выберите город':
            self.main_text.setText('Пожалуйста укажите город.')
        else:
            self.main_text.setText('Вы выбрали город \n {}'.format(self.value))
             # Основная часть программы


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
