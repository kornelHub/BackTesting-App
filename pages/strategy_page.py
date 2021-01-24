import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/strategy_page.ui"))


class Strategy_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.p2_buyCondition_treeWidget.setHeaderLabel("")
        self.p2_sellCondition_treeWidget.setHeaderLabel("")

        #Buy
        self.p2_add_buy_rule.setIcon(QtGui.QIcon('icons/add.png'))
        self.p2_add_buy_rule.setIconSize(QtCore.QSize(24, 24))

        self.p2_edit_buy_rule.setIcon(QtGui.QIcon('icons/edit.png'))
        self.p2_edit_buy_rule.setIconSize(QtCore.QSize(24, 24))

        self.p2_delete_buy_rule.setIcon(QtGui.QIcon('icons/trash.png'))
        self.p2_delete_buy_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_delete_buy_rule.clicked.connect(self.delete_buy_rule)

        self.p2_undo_buy_rule.setIcon(QtGui.QIcon('icons/undo.png'))
        self.p2_undo_buy_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_undo_buy_rule.clicked.connect(self.undo_buy_rule)


        #Sell
        self.p2_add_sell_rule.setIcon(QtGui.QIcon('icons/add.png'))
        self.p2_add_sell_rule.setIconSize(QtCore.QSize(24, 24))

        self.p2_edit_sell_rule.setIcon(QtGui.QIcon('icons/edit.png'))
        self.p2_edit_sell_rule.setIconSize(QtCore.QSize(24, 24))

        self.p2_delete_sell_rule.setIcon(QtGui.QIcon('icons/trash.png'))
        self.p2_delete_sell_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_delete_sell_rule.clicked.connect(self.delete_sell_rule)

        self.p2_undo_sell_rule.setIcon(QtGui.QIcon('icons/undo.png'))
        self.p2_undo_sell_rule.setIconSize(QtCore.QSize(24, 24))
        self.p2_undo_sell_rule.clicked.connect(self.undo_sell_rule)

        # init sell treeView
        self.sell_level_1 = QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget, ["SMA (7, Open) [+0] >= SMA (7, Open) [-1]"])
        self.sell_level_2 = QtWidgets.QTreeWidgetItem(self.sell_level_1, ["EMA (7, Open) [+0] >= EMA (7, Open) [-1]"])
        self.sell_level_3 = QtWidgets.QTreeWidgetItem(self.sell_level_2, ["WR (14) [+0] > SMA (7, Open) [+0]"])
        self.sell_level_2_1 = QtWidgets.QTreeWidgetItem(self.sell_level_1, ["BOLL - Upper Band (21, 2) [+0] >= BOLL - Lower Band (21, 2) [-1]"])
        self.p2_sellCondition_treeWidget.expandAll()

        # init buy treeView
        self.buy_level_1 = QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget, ["SMA (7, Open) [+0] <= SMA (7, Open) [-1]"])
        self.buy_level_2 = QtWidgets.QTreeWidgetItem(self.buy_level_1, ["EMA (7, Open) [+0] <= EMA (7, Open) [-1]"])
        self.buy_level_3 = QtWidgets.QTreeWidgetItem(self.buy_level_2, ["WR (14) [+0] < SMA (7, Open) [+0]"])
        self.buy_level_2_1 = QtWidgets.QTreeWidgetItem(self.buy_level_1, ["MACD - Singal Line (12, 26, 9, Open) [+0] >= MACD - MACD Line (12, 26, 9, Open) [-1]"])
        self.buy_level_2_3 = QtWidgets.QTreeWidgetItem(self.buy_level_1, ["Open (-) [+0] >= Value (15555) [+0]"])
        self.p2_buyCondition_treeWidget.expandAll()

        # sell_level_1.setBackground(0, QtGui.QColor(170, 14, 9))
        # sell_level_2.setBackground(0, QtGui.QColor(220, 9, 9))
        # sell_level_3.setBackground(0, QtGui.QColor(246, 35, 35))
        # sell_level_4.setBackground(0, QtGui.QColor(248, 84, 84))

########################################################################################################################

    def delete_buy_rule(self):
        print('delete_buy_rule')
        root = self.p2_buyCondition_treeWidget.invisibleRootItem()
        for item in self.p2_buyCondition_treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    def undo_buy_rule(self):
        print('undo buy rule')

########################################################################################################################

    def delete_sell_rule(self):
        print('delete_sell_rule')
        root = self.p2_sellCondition_treeWidget.invisibleRootItem()
        for item in self.p2_sellCondition_treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    def undo_sell_rule(self):
        print('undo sell rule')

########################################################################################################################

if __name__ == '__strategy_page__':
    import sys
    print('+++strategy_page')
    app = QtGui.QGuiApplication(sys.argv)
    w = Strategy_Widget()
    w.show()
    sys.exit(app.exec_())