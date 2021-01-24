import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtCore import Slot
from pages.add_strategy_rule_page import Add_Strategy_Rule_Widget

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/strategy_page.ui"))


class Strategy_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.p2_buyCondition_treeWidget.setHeaderLabel("")
        self.p2_sellCondition_treeWidget.setHeaderLabel("")
        self.helper_on_adding_new_rules = False

        # Buy
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

        # Sell
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

    def display_add_strategy_rule_page_buy_context(self, strategy_page_object):
        self.receive_buy_strategy_rule_to_add_object = Receive_Buy_Strategy_Rule_To_Add()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        list_of_items_in_buy_qtreewidget = self.p2_buyCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
        add_strategy_page_widget.load_qtreewidget(list_of_items_in_buy_qtreewidget)
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(lambda: add_strategy_page_widget.add_new_rule(self.receive_buy_strategy_rule_to_add_object, strategy_page_object))

    def display_add_strategy_rule_page_modify_buy_context(self):
        receive_strategy_rule_to_modify_object = Receive_Strategy_Rule_To_Modify()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        add_strategy_page_widget.load_rule_details_to_modify(self.p2_buyCondition_treeWidget.currentItem().text(0))
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(lambda: add_strategy_page_widget.save_modified_rule(
            self.p2_buyCondition_treeWidget.currentItem(), receive_strategy_rule_to_modify_object))

    def delete_buy_rule(self):
        print('delete_buy_rule')
        root = self.p2_buyCondition_treeWidget.invisibleRootItem()
        for item in self.p2_buyCondition_treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    def undo_buy_rule(self):
        print('undo buy rule')

########################################################################################################################

    def display_add_strategy_rule_page_sell_context(self, strategy_page_object):
        self.receive_sell_strategy_rule_to_add_object = Receive_Sell_Strategy_Rule_To_Add()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        list_of_items_in_sell_qtreewidget = self.p2_sellCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
        add_strategy_page_widget.load_qtreewidget(list_of_items_in_sell_qtreewidget)
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(lambda: add_strategy_page_widget.add_new_rule(self.receive_sell_strategy_rule_to_add_object, strategy_page_object))

    def display_add_strategy_rule_page_modify_sell_context(self):
        receive_strategy_rule_to_modify_object = Receive_Strategy_Rule_To_Modify()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        add_strategy_page_widget.load_rule_details_to_modify(self.p2_sellCondition_treeWidget.currentItem().text(0))
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(lambda: add_strategy_page_widget.save_modified_rule(
            self.p2_sellCondition_treeWidget.currentItem(), receive_strategy_rule_to_modify_object))

    def delete_sell_rule(self):
        print('delete_sell_rule')
        root = self.p2_sellCondition_treeWidget.invisibleRootItem()
        for item in self.p2_sellCondition_treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    def undo_sell_rule(self):
        print('undo sell rule')

########################################################################################################################

    def add_parent_text_to_list(self, qTreeWidgetItem, list):
        if len(list) > 0:
            if qTreeWidgetItem.parent() is not None:
                if qTreeWidgetItem.parent().text(0) == list[0]:
                    self.add_parent_text_to_list(qTreeWidgetItem.parent(), list[1:])
                else:
                    self.helper_on_adding_new_rules = False
                    return False
            else:
                self.helper_on_adding_new_rules = True
                return True
        else:
            self.helper_on_adding_new_rules = True
            return True

########################################################################################################################


# Add new rule receivers
class Receive_Buy_Strategy_Rule_To_Add(QtCore.QObject):
    @Slot(str)
    def receive_and_add_rule(self, received_rule, text_of_parent_element, strategy_page_object):
        if len(text_of_parent_element) > 0:
            for list_in_list in text_of_parent_element:
                if len(list_in_list) > 0:
                    for found_element in strategy_page_object.p2_buyCondition_treeWidget.findItems(
                            list_in_list[0], QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0):
                        strategy_page_object.add_parent_text_to_list(found_element, list_in_list[1:])
                        if strategy_page_object.helper_on_adding_new_rules:
                            QtWidgets.QTreeWidgetItem(found_element, [received_rule])
        else:
            QtWidgets.QTreeWidgetItem(strategy_page_object.p2_buyCondition_treeWidget, [received_rule])
        strategy_page_object.p2_buyCondition_treeWidget.expandAll()


class Receive_Sell_Strategy_Rule_To_Add(QtCore.QObject):
    @Slot(str)
    def receive_and_add_rule(self, received_rule, text_of_parent_element, strategy_page_object):
        if len(text_of_parent_element) > 0:
            for list_in_list in text_of_parent_element:
                if len(list_in_list) > 0:
                    for found_element in strategy_page_object.p2_sellCondition_treeWidget.findItems(
                            list_in_list[0], QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0):
                        strategy_page_object.add_parent_text_to_list(found_element, list_in_list[1:])
                        if strategy_page_object.helper_on_adding_new_rules:
                            QtWidgets.QTreeWidgetItem(found_element, [received_rule])
        else:
            QtWidgets.QTreeWidgetItem(strategy_page_object.p2_sellCondition_treeWidget, [received_rule])
        strategy_page_object.p2_sellCondition_treeWidget.expandAll()


# Modify rule receiver
class Receive_Strategy_Rule_To_Modify(QtCore.QObject):
    @Slot(str)
    def receive_and_modify_rule(self, received_rule, current_selected_item):
        current_selected_item.setText(0, received_rule)


if __name__ == '__strategy_page__':
    import sys
    app = QtGui.QGuiApplication(sys.argv)
    w = Strategy_Widget()
    w.show()
    sys.exit(app.exec_())