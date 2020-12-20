import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QFileDialog
from binance.helpers import date_to_milliseconds
from binance_api import fetch_data
import plot_data
from functools import partial
import pages.strategy_page
from pages.ui_functions import *

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/buy_strategy.ui"))

class Buy_Strategy_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.p2_add_buy_rule.setIcon(QtGui.QIcon('icons/add.png'))
        self.p2_add_buy_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_add_buy_rule.clicked.connect(lambda : pages.strategy_page.Strategy_Widget().display_rule_form_for_buy_strategy())

        self.p2_edit_buy_rule.setIcon(QtGui.QIcon('icons/edit.png'))
        self.p2_edit_buy_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_edit_buy_rule.clicked.connect(self.edit_buy_rule)

        self.p2_delete_buy_rule.setIcon(QtGui.QIcon('icons/trash.png'))
        self.p2_delete_buy_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_delete_buy_rule.clicked.connect(self.delete_buy_rule)

        self.p2_undo_buy_rule.setIcon(QtGui.QIcon('icons/undo.png'))
        self.p2_undo_buy_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_undo_buy_rule.clicked.connect(self.undo_buy_rule)


    # def add_buy_rule(self):
    #

    def edit_buy_rule(self):
        print('edit buy rule')

    def delete_buy_rule(self):
        print('delete_buy_rule')
        root = self.p2_buyCondition_treeWidget.invisibleRootItem()
        for item in self.p2_buyCondition_treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    def undo_buy_rule(self):
        print('undo buy rule')


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Buy_Strategy_Widget()
    w.show()
    sys.exit(app.exec_())
