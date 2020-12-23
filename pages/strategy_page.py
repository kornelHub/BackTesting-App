import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType, QUiLoader
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/strategy_page.ui"))


class Strategy_Widget(Base, Form):
    buy_stackedWidget_object = None
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        buy_stackedWidget_object = QtWidgets.QStackedWidget()
        buy_stackedWidget_object = self.strategy_page_buy_stackedWidget
        print('current widget', buy_stackedWidget_object.currentWidget())
        print('class!', type(self))

    def display_rule_form_for_buy_strategy(self):
        objectSP = Strategy_Widget()
        print('KDDDDD')
        print('funcion! ',type(objectSP))
        objectSP.buy_stackedWidget_object.setCurrentIndex(1)




if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Strategy_Widget()
    w.show()
    sys.exit(app.exec_())