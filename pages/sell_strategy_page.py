import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QFileDialog


from pages.strategy_page import *

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/sell_strategy.ui"))

class Sell_Strategy_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

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

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Sell_Strategy_Widget()
    w.show()
    sys.exit(app.exec_())
