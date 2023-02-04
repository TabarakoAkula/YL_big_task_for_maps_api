import sys
from PyQt5 import QtWidgets
from window import Ui_MainWindow

longitude, width = input('Введите долготу и широту: ').split()


def load_window():
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())


load_window()

