import os
from PySide2 import QtGui, QtWidgets, QtWebEngineWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from functools import partial

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "ui/mainWindow.ui"))

class MainWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)


        buttons = (self.btn_menu_page_2, self.btn_menu_page_3)
        for i, button in enumerate(buttons):
            button.clicked.connect(partial(self.widget_pages.setCurrentIndex, i))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())