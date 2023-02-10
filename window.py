from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel
import keyboard
import requests


class Ui_MainWindow(object):
    scale = 1
    size = 1

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.longitude, self.latitude = input('Введите долготу и широту: ').split()
        self.size = int(input('Введите размер(1-17): '))
        self.label = QLabel(self.centralwidget)
        if self.size > 17:
            self.size = 17
        if self.size < 1:
            self.size = 1
        self.get()
        self.label.move(75, 75)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        keyboard.on_press_key("PgUp", lambda _: self.change_value("up"))
        keyboard.on_press_key("PgDown", lambda _: self.change_value("down"))
        keyboard.on_press_key("UP", lambda _: self.change_coordinates("Up"))
        keyboard.on_press_key("DOWN", lambda _: self.change_coordinates("Down"))
        keyboard.on_press_key("LEFT", lambda _: self.change_coordinates("Left"))
        keyboard.on_press_key("RIGHT", lambda _: self.change_coordinates("Right"))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MapViewer"))

    def change_value(self, name):
        self.scale = name
        if self.scale == 'up':
            self.size += 1
        else:
            self.size -= 1
        if self.size > 17:
            self.size = 17
        if self.size < 1:
            self.size = 1
        self.get()

    def change_coordinates(self, name):
        self.cor = name
        if self.size >= 8:
            self.del_longitude = 90 / self.size ** 2 / 30
            self.del_latitude = 90 / self.size ** 2 / 30
        else:
            self.del_longitude = 90 / self.size / 10
            self.del_latitude = 90 / self.size / 10
        print(self.del_latitude, self.del_longitude)
        if name == 'Right':
            if float(self.longitude) + self.del_longitude <= 180:
                self.longitude = str(float(self.longitude) + self.del_longitude)
        if name == 'Left':
            if float(self.longitude) - self.del_longitude >= -180:
                self.longitude = str(float(self.longitude) - self.del_longitude)
        if name == 'Down':
            if float(self.latitude) - self.del_latitude >= -90:
                self.latitude = str(float(self.latitude) - self.del_latitude)
        if name == 'Up':
            if float(self.latitude) + self.del_latitude <= 90:
                self.latitude = str(float(self.latitude) + self.del_latitude)
        self.get()


    def get(self):
        link = f'https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.latitude}&size=650,450&l=map&z={self.size}'
        response = requests.get(link)
        with open('map.png', 'wb') as file:
            file.write(response.content)
        pixmap = QtGui.QPixmap('map.png')
        if not pixmap.isNull():
            self.label.setPixmap(pixmap)
            self.label.adjustSize()
            self.label.resize(pixmap.size())


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
