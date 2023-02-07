from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap
from PIL import Image
import keyboard
import requests
import shutil


class Ui_MainWindow(object):
    scale = 1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.longitude, self.latitude = input('Введите долготу и широту: ').split()
        self.size = int(input('Введите размер(1-17): '))
        if self.size > 17:
            self.size = 17
        if self.size < 1:
            self.size = 1
        self.get()
        self.fname = 'map.png'
        self.img = Image.open(self.fname)
        self.image = QLabel(self.centralwidget)
        self.image.move(75, 75)
        self.image.resize(650, 450)
        self.pixmap = QPixmap(self.fname)
        self.image.setPixmap(self.pixmap)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        keyboard.on_press_key("UP", lambda _: self.change_value("up"))
        keyboard.on_press_key("DOWN", lambda _: self.change_value("down"))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MapViewer"))

    def change_value(self, name):
        self.scale = name
        #  if ... : ...
        #  изменение запроса карты

    def get(self):
        link = f'https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.latitude}&size=650,450&l=map&z={self.size}'
        response = requests.get(link)
        with open('map.png', 'wb') as file:
            file.write(response.content)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
