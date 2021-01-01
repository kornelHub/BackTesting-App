import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtCore import Slot
import pages.add_strategy_rule_page

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/strategy_page.ui"))


class Strategy_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        print('-----', self)
        #Buy
        self.p2_add_buy_rule.setIcon(QtGui.QIcon('icons/add.png'))
        self.p2_add_buy_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_add_buy_rule.clicked.connect(self.display_add_buy_rule_page)

        self.p2_edit_buy_rule.setIcon(QtGui.QIcon('icons/edit.png'))
        self.p2_edit_buy_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_edit_buy_rule.clicked.connect(self.edit_buy_rule)

        self.p2_delete_buy_rule.setIcon(QtGui.QIcon('icons/trash.png'))
        self.p2_delete_buy_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_delete_buy_rule.clicked.connect(self.delete_buy_rule)

        self.p2_undo_buy_rule.setIcon(QtGui.QIcon('icons/undo.png'))
        self.p2_undo_buy_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_undo_buy_rule.clicked.connect(self.undo_buy_rule)


        #Sell
        self.p2_add_sell_rule.setIcon(QtGui.QIcon('icons/add.png'))
        self.p2_add_sell_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_add_sell_rule.clicked.connect(self.display_add_sell_rule_page)

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
        self.sell_level_1 = QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget, ["lorem ipsu"])
        self.sell_level_1_2 = QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget, ["lorem ipsu222222"])
        self.sell_level_1_3 = QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget, ["lorem ipsu333333"])
        self.sell_level_2 = QtWidgets.QTreeWidgetItem(self.sell_level_1, [
            "lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2"])
        self.sell_level_3 = QtWidgets.QTreeWidgetItem(self.sell_level_2, ["lorem ipsu3"])
        self.sell_level_4 = QtWidgets.QTreeWidgetItem(self.sell_level_3, ["lorem ipsu4"])

        self.sell_level_4_2 = QtWidgets.QTreeWidgetItem(["lorem ipsu41"])
        self.sell_level_2.addChild(self.sell_level_4_2)
        self.p2_sellCondition_treeWidget.expandAll()


        # sell_level_1.setBackground(0, QtGui.QColor(170, 14, 9))
        # sell_level_2.setBackground(0, QtGui.QColor(220, 9, 9))
        # sell_level_3.setBackground(0, QtGui.QColor(246, 35, 35))
        # sell_level_4.setBackground(0, QtGui.QColor(248, 84, 84))

########################################################################################################################

    def display_add_buy_rule_page(self):
        self.window = pages.add_strategy_rule_page.Add_Strategy_Rule_Widget()
        self.window.show()


    def add_buy_rule_to_QTreeWidget(self, rule_to_add):
        print('**********************************************************')
        print(rule_to_add)
        print(self.p2_buyCondition_treeWidget.selectedItems())

    def edit_buy_rule(self):
        print('edit buy rule')

    def delete_buy_rule(self):
        print('delete_buy_rule')
        root = self.p2_buyCondition_treeWidget.invisibleRootItem()
        for item in self.p2_buyCondition_treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    def undo_buy_rule(self):
        print('undo buy rule')

########################################################################################################################
    def display_add_sell_rule_page(self):
        self.window = pages.add_strategy_rule_page.Add_Strategy_Rule_Widget()
        self.window.show()

    def add_sell_rule_to_QTreeWidget(self, rule_to_add):
        print('**********************************************************')
        print(rule_to_add)
        print(self.p2_sellCondition_treeWidget.selectedIndexes())

    def edit_sell_rule(self):
        print('edit sell rule')

    def delete_sell_rule(self):
        print('delete_sell_rule')
        root = self.p2_sellCondition_treeWidget.invisibleRootItem()
        for item in self.p2_sellCondition_treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    def undo_sell_rule(self):
        print('undo sell rule')

########################################################################################################################

class Receive_Strategy_Rule(QtCore.QObject):
    @Slot(str)
    def on_recive(self, received_rule):
        print('Odebrano:', received_rule)

if __name__ == '__strategy_page__':
    import sys
    print('+++strategy_page')
    app = QtGui.QGuiApplication(sys.argv)
    w = Strategy_Widget()
    w.show()
    sys.exit(app.exec_())