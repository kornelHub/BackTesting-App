import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QFileDialog
from binance.helpers import date_to_milliseconds
from binance_api import fetch_data
import plot_data

from pages.strategy_page import *
from pages.ui_functions import *

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/sell_strategy.ui"))

class Sell_Strategy_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        self.p2_add_sell_rule.setIcon(QtGui.QIcon('icons/add.png'))
        self.p2_add_sell_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_add_sell_rule.clicked.connect(self.add_sell_condition)

        self.p2_edit_sell_rule.setIcon(QtGui.QIcon('icons/edit.png'))
        self.p2_edit_sell_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_edit_sell_rule.clicked.connect(self.edit_sell_rule)

        self.p2_delete_sell_rule.setIcon(QtGui.QIcon('icons/trash.png'))
        self.p2_delete_sell_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_delete_sell_rule.clicked.connect(self.delete_sell_rule)

        self.p2_undo_sell_rule.setIcon(QtGui.QIcon('icons/undo.png'))
        self.p2_undo_sell_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_undo_sell_rule.clicked.connect(self.undo_sell_rule)

        #init treeView
        sell_level_1 = QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget, ["lorem ipsu"])
        sell_level_2 = QtWidgets.QTreeWidgetItem(sell_level_1, [
            "lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2"])
        sell_level_3 = QtWidgets.QTreeWidgetItem(sell_level_2, ["lorem ipsu3"])
        sell_level_4 = QtWidgets.QTreeWidgetItem(sell_level_3, ["lorem ipsu4"])

        sell_level_4_2 = QtWidgets.QTreeWidgetItem(["lorem ipsu41"])
        sell_level_2.addChild(sell_level_4_2)
        self.p2_sellCondition_treeWidget.expandAll()


        # sell_level_1.setBackground(0, QtGui.QColor(170, 14, 9))
        # sell_level_2.setBackground(0, QtGui.QColor(220, 9, 9))
        # sell_level_3.setBackground(0, QtGui.QColor(246, 35, 35))
        # sell_level_4.setBackground(0, QtGui.QColor(248, 84, 84))

    def add_sell_condition(self):
        print('add sell rule')

    def edit_sell_rule(self):
        print('edit sell rule')

    def delete_sell_rule(self):
        print('delete_sell_rule')
        root = self.p2_sellCondition_treeWidget.invisibleRootItem()
        for item in self.p2_sellCondition_treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    def undo_sell_rule(self):
        print('undo sell rule')


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Sell_Strategy_Widget()
    w.show()
    sys.exit(app.exec_())
