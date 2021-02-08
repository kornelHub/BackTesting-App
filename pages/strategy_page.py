import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtCore import Slot
from pages.add_strategy_rule_page import Add_Strategy_Rule_Widget
from engine.simulation import get_buy_rules, get_sell_rules
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/strategy_page.ui"))


class Strategy_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.p2_buyCondition_treeWidget.setHeaderLabel("")
        self.p2_sellCondition_treeWidget.setHeaderLabel("")
        self.helper_on_adding_new_rules = False
        QtWidgets.QToolTip.setFont(QtGui.QFont('MS Shell Dlg 2', 10))
        self.stop_loss_checkbox.stateChanged.connect(lambda: self.check_if_disabled_needed_for_settings_fields(self.stop_loss_checkbox.isChecked(), self.sell_stop_loss_lineEdit_1, self.sell_stop_loss_comboBox_2))
        self.take_profit_checkbox.stateChanged.connect(lambda: self.check_if_disabled_needed_for_settings_fields(self.take_profit_checkbox.isChecked(), self.sell_take_profit_lineEdit_1, self.sell_take_profit_comboBox_2))

        # dev helper
        self.buy_commission_lineEdit_1.setText('0.1')
        self.buy_balance_lineEdit2.setText('1')
        self.sell_commission_lineEdit_1.setText('0.1')
        self.sell_balance_lineEdit.setText('10000')
        self.sell_stop_loss_lineEdit_1.setText('14')
        self.sell_take_profit_lineEdit_1.setText('14')

        # Buy
        self.p2_add_buy_rule.setIcon(QtGui.QIcon('icons/add.png'))
        self.p2_add_buy_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_add_buy_rule.setToolTip('Add new buy rule')

        self.p2_copy_buy_rule.setIcon(QtGui.QIcon('icons/copy.png'))
        self.p2_copy_buy_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_copy_buy_rule.clicked.connect(lambda: self.copy_buy_rule())
        self.p2_copy_buy_rule.setToolTip('Copy selected rule')

        self.p2_edit_buy_rule.setIcon(QtGui.QIcon('icons/edit.png'))
        self.p2_edit_buy_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_edit_buy_rule.setToolTip('Edit selected buy rule')

        self.p2_delete_buy_rule.setIcon(QtGui.QIcon('icons/trash.png'))
        self.p2_delete_buy_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_delete_buy_rule.clicked.connect(lambda: self.delete_buy_rule())
        self.p2_delete_buy_rule.setToolTip('Remove selected buy rule')

        self.p2_save_strategy_1.setIcon(QtGui.QIcon('icons/save.png'))
        self.p2_save_strategy_1.setIconSize(QtCore.QSize(32, 32))
        self.p2_save_strategy_1.clicked.connect(lambda: self.save_rules_to_json_file())
        self.p2_save_strategy_1.setToolTip('Save buy and sell rules to file')

        self.p2_load_strategy_1.setIcon(QtGui.QIcon('icons/load.png'))
        self.p2_load_strategy_1.setIconSize(QtCore.QSize(32, 32))
        self.p2_load_strategy_1.clicked.connect(lambda: self.load_rules_from_json_file())
        self.p2_load_strategy_1.setToolTip('Load buy and sell rules from file')

        # Sell
        self.p2_add_sell_rule.setIcon(QtGui.QIcon('icons/add.png'))
        self.p2_add_sell_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_add_sell_rule.setToolTip('Add new sell rule')

        self.p2_copy_sell_rule.setIcon(QtGui.QIcon('icons/copy.png'))
        self.p2_copy_sell_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_copy_sell_rule.clicked.connect(lambda: self.copy_sell_rule())
        self.p2_copy_sell_rule.setToolTip('Copy selected rule')

        self.p2_edit_sell_rule.setIcon(QtGui.QIcon('icons/edit.png'))
        self.p2_edit_sell_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_edit_sell_rule.setToolTip('Edit selected sell rule')

        self.p2_delete_sell_rule.setIcon(QtGui.QIcon('icons/trash.png'))
        self.p2_delete_sell_rule.setIconSize(QtCore.QSize(32, 32))
        self.p2_delete_sell_rule.clicked.connect(lambda: self.delete_sell_rule())
        self.p2_delete_sell_rule.setToolTip('Remove selected sell rule')

        self.p2_save_strategy_2.setIcon(QtGui.QIcon('icons/save.png'))
        self.p2_save_strategy_2.setIconSize(QtCore.QSize(32, 32))
        self.p2_save_strategy_2.clicked.connect(lambda: self.save_rules_to_json_file())
        self.p2_save_strategy_2.setToolTip('Save buy and sell rules to file')

        self.p2_load_strategy_2.setIcon(QtGui.QIcon('icons/load.png'))
        self.p2_load_strategy_2.setIconSize(QtCore.QSize(32, 32))
        self.p2_load_strategy_2.clicked.connect(lambda: self.load_rules_from_json_file())
        self.p2_load_strategy_2.setToolTip('Load buy and sell rules from file')

        # init sell treeView
        self.sell_level_1 = QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget, ["SMA (7, Open) [0] >= SMA (7, Open) [-1]"])
        self.sell_level_2 = QtWidgets.QTreeWidgetItem(self.sell_level_1, ["EMA (7, Open) [0] >= EMA (7, Open) [-1]"])
        self.sell_level_3 = QtWidgets.QTreeWidgetItem(self.sell_level_2, ["WR (14) [0] > SMA (7, Open) [0]"])
        self.sell_level_2_1 = QtWidgets.QTreeWidgetItem(self.sell_level_1, ["BOLL - Upper Band (21, 2) [0] >= BOLL - Lower Band (21, 2) [-1]"])
        self.p2_sellCondition_treeWidget.expandAll()

        # init buy treeView
        self.buy_level_1 = QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget, ["SMA (7, Open) [0] <= SMA (7, Open) [-1]"])
        self.buy_level_2 = QtWidgets.QTreeWidgetItem(self.buy_level_1, ["EMA (7, Open) [0] <= EMA (7, Open) [-1]"])
        self.buy_level_3 = QtWidgets.QTreeWidgetItem(self.buy_level_2, ["WR (14) [0] < SMA (7, Open) [0]"])
        self.buy_level_2_1 = QtWidgets.QTreeWidgetItem(self.buy_level_1, ["MACD - Singal Line (12, 26, 9, Open) [0] >= MACD - MACD Line (12, 26, 9, Open) [-1]"])
        self.buy_level_2_3 = QtWidgets.QTreeWidgetItem(self.buy_level_1, ["Open (-) [0] >= Value (15555) [0]"])
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

    def copy_buy_rule(self):
        if self.p2_buyCondition_treeWidget.selectedItems()[0].parent() is None:
            QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget, [self.p2_buyCondition_treeWidget.selectedItems()[0].text(0)])
        else:
            QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget.selectedItems()[0].parent(), [self.p2_buyCondition_treeWidget.selectedItems()[0].text(0)])

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

    def save_rules_to_json_file(self):
        # get buy rules and convert qTreeWidgetItems to string
        buy_rules = get_buy_rules(self)
        for x in range(len(buy_rules['buy_rules'])):
            buy_rules['buy_rules'][x]['qTreeWidgetItem'] = str(buy_rules['buy_rules'][x]['qTreeWidgetItem'])
            buy_rules['buy_rules'][x]['qTreeWidgetItem_Parent'] = str(buy_rules['buy_rules'][x]['qTreeWidgetItem_Parent'])

        # get sell rules and convert qTreeWidgetItems to string
        sell_rules = get_sell_rules(self)
        for x in range(len(sell_rules['sell_rules'])):
            sell_rules['sell_rules'][x]['qTreeWidgetItem'] = str(sell_rules['sell_rules'][x]['qTreeWidgetItem'])
            sell_rules['sell_rules'][x]['qTreeWidgetItem_Parent'] = str(sell_rules['sell_rules'][x]['qTreeWidgetItem_Parent'])

        path_to_file = QtWidgets.QFileDialog.getSaveFileName(self, 'Save strategy to JSON file', current_dir[:-6] + '\data\strategy', 'JSON Files (*.json)')
        combined_rules = {'buy_rules': [], 'sell_rules': []}
        combined_rules['buy_rules'].append(buy_rules['buy_rules'])
        combined_rules['sell_rules'].append(sell_rules['sell_rules'])
        with open(path_to_file[0], 'w') as file:
            json.dump(combined_rules, file, indent=4)

########################################################################################################################

    def display_add_strategy_rule_page_sell_context(self, strategy_page_object):
        self.receive_sell_strategy_rule_to_add_object = Receive_Sell_Strategy_Rule_To_Add()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        list_of_items_in_sell_qtreewidget = self.p2_sellCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
        add_strategy_page_widget.load_qtreewidget(list_of_items_in_sell_qtreewidget)
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(lambda: add_strategy_page_widget.add_new_rule(self.receive_sell_strategy_rule_to_add_object, strategy_page_object))

    def copy_sell_rule(self):
        if self.p2_sellCondition_treeWidget.selectedItems()[0].parent() is None:
            QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget, [self.p2_sellCondition_treeWidget.selectedItems()[0].text(0)])
        else:
            QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget.selectedItems()[0].parent(), [self.p2_sellCondition_treeWidget.selectedItems()[0].text(0)])

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

    def load_rules_from_json_file(self):
        path_to_json_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Load strategy from JSON file', current_dir[:-6] + '\data\strategy', 'JSON Files (*.json)')
        with open(path_to_json_file[0]) as json_file:
            loaded_rules = json.load(json_file)

        # clear both QTreeWidgets
        self.p2_buyCondition_treeWidget.clear()
        self.p2_sellCondition_treeWidget.clear()
        buy_rules = loaded_rules['buy_rules'][0]
        sell_rules = loaded_rules['sell_rules'][0]
        QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget, [buy_rules[0]['rule_text']])
        for x in range(len(buy_rules)-1):
            for y in range(len(buy_rules)):
                if buy_rules[x+1]['qTreeWidgetItem_Parent'] == buy_rules[y]['qTreeWidgetItem']:
                    found_parent = buy_rules[y]['rule_text']
            QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget.findItems(found_parent, QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)[-1], [buy_rules[x+1]['rule_text']])

        QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget, [sell_rules[0]['rule_text']])
        for x in range(len(sell_rules)-1):
            for y in range(len(sell_rules)):
                if sell_rules[x+1]['qTreeWidgetItem_Parent'] == sell_rules[y]['qTreeWidgetItem']:
                    found_parent = sell_rules[y]['rule_text']
            QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget.findItems(found_parent, QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)[-1], [sell_rules[x+1]['rule_text']])

            self.p2_buyCondition_treeWidget.expandAll()
            self.p2_sellCondition_treeWidget.expandAll()

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
    def check_if_disabled_needed_for_settings_fields(self, is_checked, value_line_edit, unit_dropdown):
        if is_checked:
            value_line_edit.setReadOnly(False)
            unit_dropdown.setEnabled(True)
        else:
            value_line_edit.setReadOnly(True)
            unit_dropdown.setEnabled(False)

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