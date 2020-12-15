import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType, QUiLoader
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/strategy_page.ui"))


class Strategy_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)

        #Buy
        self.p2_add_buy_rule.setIcon(QtGui.QIcon('icons/add.png'))
        self.p2_add_buy_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_add_buy_rule.clicked.connect(self.add_buy_rule)

        self.p2_edit_buy_rule.setIcon(QtGui.QIcon('icons/edit.png'))
        self.p2_edit_buy_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_edit_buy_rule.clicked.connect(self.edit_buy_rule)

        self.p2_delete_buy_rule.setIcon(QtGui.QIcon('icons/trash.png'))
        self.p2_delete_buy_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_delete_buy_rule.clicked.connect(self.delete_buy_rule)


        #Sell
        self.p2_add_sell_rule.setIcon(QtGui.QIcon('icons/add.png'))
        self.p2_add_sell_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_add_sell_rule.clicked.connect(self.add_sell_condition)

        self.p2_edit_sell_rule.setIcon(QtGui.QIcon('icons/edit.png'))
        self.p2_edit_sell_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_edit_sell_rule.clicked.connect(self.edit_sell_rule)

        self.p2_delete_sell_rule.setIcon(QtGui.QIcon('icons/trash.png'))
        self.p2_delete_sell_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_delete_sell_rule.clicked.connect(self.delete_sell_rule)


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


    def add_buy_rule(self):
        self.p2_rightBottom_widget.hide()
        self.p2_rightTop_widget.hide()
        self.p2_right_widget = QUiLoader().load('ui/add_strategy_rule_page.ui', self.p2_right_widget)
        self.p2_right_widget.setContentsMargins(0, 0, 0, 0)
        self.p2_right_widget.show()

    def edit_buy_rule(self):
        print('edit buy rule')

    def delete_buy_rule(self):
        print('delete_buy_rule')


    def add_sell_condition(self):
        self.p2_leftTop_widget.hide()
        self.p2_leftBottom_widget.hide()
        self.p2_left_widget = QUiLoader().load('ui/add_strategy_rule_page.ui', self.p2_left_widget)
        self.p2_left_widget.show()
        self.p3_sellCondition_treeWidget = self.p2_sellCondition_treeWidget
        self.p3_sellCondition_treeWidget.show()

    def edit_sell_rule(self):
        print('edit sell rule')

    def delete_sell_rule(self):
        print('delete_sell_rule')


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Strategy_Widget()
    w.show()
    sys.exit(app.exec_())