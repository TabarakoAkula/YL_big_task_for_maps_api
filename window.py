from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit
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
        self.type = 'map'
        if self.size > 17:
            self.size = 17
        if self.size < 1:
            self.size = 1
        self.get()
        self.label.move(75, 75)
        self.pushbutton_scheme = QPushButton(self.centralwidget)
        self.pushbutton_satellite = QPushButton(self.centralwidget)
        self.pushbutton_hybrid = QPushButton(self.centralwidget)
        self.pushbutton_scheme.move(75, 540)
        self.pushbutton_satellite.move(340, 540)
        self.pushbutton_hybrid.move(585, 540)
        self.pushbutton_scheme.resize(140, 30)
        self.pushbutton_satellite.resize(140, 30)
        self.pushbutton_hybrid.resize(140, 30)
        self.search_lineedit = QLineEdit(self.centralwidget)
        self.search_lineedit.resize(605, 30)
        self.search_lineedit.move(75, 30)
        self.search_button = QPushButton(self.centralwidget)
        self.search_button.move(687, 30)
        self.search_button.resize(35, 32)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        keyboard.on_press_key("PgUp", lambda _: self.change_value("up"))
        keyboard.on_press_key("PgDown", lambda _: self.change_value("down"))
        keyboard.on_press_key("UP", lambda _: self.change_coordinates("Up"))
        keyboard.on_press_key("DOWN", lambda _: self.change_coordinates("Down"))
        keyboard.on_press_key("LEFT", lambda _: self.change_coordinates("Left"))
        keyboard.on_press_key("RIGHT", lambda _: self.change_coordinates("Right"))
        self.pushbutton_hybrid.clicked.connect(lambda: self.change_map_type('skl'))
        self.pushbutton_scheme.clicked.connect(lambda: self.change_map_type('map'))
        self.pushbutton_satellite.clicked.connect(lambda: self.change_map_type('sat'))
        self.search_button.clicked.connect(lambda: self.find_object())

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MapViewer"))
        self.pushbutton_scheme.setText(_translate("mainWindow", "Scheme"))
        self.pushbutton_satellite.setText(_translate("mainWindow", "Satellite"))
        self.pushbutton_hybrid.setText(_translate("mainWindow", "Hybrid"))
        self.search_button.setText(_translate('mainWindow', '🔍'))

    def change_map_type(self, type_now):
        if type_now != 'skl':
            self.type = type_now
        else:
            self.type = 'map,sat,skl'
        self.get()

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
        link = f'https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.latitude}&size=650,450&l={self.type}&z={self.size}'
        response = requests.get(link)
        with open('map.png', 'wb') as file:
            file.write(response.content)
        pixmap = QtGui.QPixmap('map.png')
        if not pixmap.isNull():
            self.label.setPixmap(pixmap)
            self.label.adjustSize()
            self.label.resize(pixmap.size())


    def find_object(self):
        self.Status = True
        self.name_to_find = self.search_lineedit.text()
        self.geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
        self.geocoder_params = {
            "apikey": api_key,
            "geocode": self.name_to_find,
            "format": "json"}
        self.response = requests.get(self.geocoder_api_server, params=self.geocoder_params)
        if not self.response:
            pass
        self.json_response = self.response.json()
        self.toponym = self.json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        self.toponym_coodrinates = self.toponym["Point"]["pos"]
        self.toponym_longitude, self.toponym_lattitude = self.toponym_coodrinates.split(" ")
        self.longitude = self.toponym_longitude
        self.latitude = self.toponym_lattitude
        self.get()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
