from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel
import keyboard
import requests


class Ui_MainWindow(object):
    scale = 1

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
        self.get(self.size)
        self.label.move(75, 75)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        keyboard.on_press_key("PgUp", lambda _: self.change_value("up"))
        keyboard.on_press_key("PgDown", lambda _: self.change_value("down"))

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
        self.get(self.size)

    def get(self, size):
        link = f'https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.latitude}&size=650,450&l=map&z={size}'
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
