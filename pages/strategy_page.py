import os
from PySide2 import QtGui, QtWidgets
from PySide2.QtUiTools import loadUiType, QUiLoader
import pandas as pd

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/strategy_page.ui"))


class Strategy_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.p2_addBuyCondition_button.clicked.connect(self.add_buy_condition)
        self.p2_addSellCondition_button.clicked.connect(self.add_sell_condition)

        #init treeView
        sell_level_1 = QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget, ["lorem ipsu"])
        sell_level_2 = QtWidgets.QTreeWidgetItem(sell_level_1, [
            "lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2"])
        sell_level_3 = QtWidgets.QTreeWidgetItem(sell_level_2, ["lorem ipsu3"])
        sell_level_4 = QtWidgets.QTreeWidgetItem(sell_level_3, ["lorem ipsu4"])

        sell_level_4_2 = QtWidgets.QTreeWidgetItem(["lorem ipsu41"])
        sell_level_2.addChild(sell_level_4_2)
        # position_df = pd.DataFrame(columns=['name', 'position', 'text'])

        sell_level_1.setBackground(0, QtGui.QColor(170, 14, 9))
        sell_level_2.setBackground(0, QtGui.QColor(220, 9, 9))
        sell_level_3.setBackground(0, QtGui.QColor(246, 35, 35))
        sell_level_4.setBackground(0, QtGui.QColor(248, 84, 84))




    def add_buy_condition(self):
        # buy_level_1 = QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget, ["lorem ipsu"])
        # buy_level_2 = QtWidgets.QTreeWidgetItem(buy_level_1, ["lorem ipsu2"])
        self.p2_rightBottom_widget.hide()
        self.p2_rightTop_widget.hide()
        size_befor = self.p2_right_widget.size()
        self.p2_right_widget = QUiLoader().load('ui/add_strategy_rule_page.ui', self.p2_right_widget)
        self.p2_right_widget.setContentsMargins(0, 0, 0, 0)
        self.p2_right_widget.show()



    def add_sell_condition(self):
        self.p2_leftTop_widget.hide()
        self.p2_leftBottom_widget.hide()
        self.p2_left_widget = QUiLoader().load('ui/add_strategy_rule_page.ui', self.p2_left_widget)
        self.p2_left_widget.show()
        self.p3_sellCondition_treeWidget = self.p2_sellCondition_treeWidget
        self.p3_sellCondition_treeWidget.show()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Strategy_Widget()
    w.show()
    sys.exit(app.exec_())
