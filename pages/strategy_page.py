import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtCore import Slot
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator
from pages.add_strategy_rule_page import Add_Strategy_Rule_Widget
from engine.simulation import get_buy_rules, get_sell_rules
from engine.simulation import get_buy_simulation_settings, get_sell_simulation_settings
import json
from pages.define_indicator_to_plot_page import Define_Indicator_To_Plot_Page
from utilities.helpers import show_error_message, hide_error_message, check_if_all_fields_have_text

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
        self.stop_loss_checkbox.stateChanged.connect(lambda:
                                                     self.check_if_disabled_needed_for_settings_fields(
                                                         self.stop_loss_checkbox.isChecked(),
                                                         self.sell_stop_loss_lineEdit_1,
                                                         self.sell_stop_loss_comboBox_2,
                                                         self.label_9))

        self.take_profit_checkbox.stateChanged.connect(lambda:
                                                       self.check_if_disabled_needed_for_settings_fields(
                                                           self.take_profit_checkbox.isChecked(),
                                                           self.sell_take_profit_lineEdit_1,
                                                           self.sell_take_profit_comboBox_2,
                                                           self.label_10))

        hide_error_message(self.error_message_label)
        self.buy_price_source_comboBox.setCurrentIndex(-1)
        self.sell_price_source_comboBox.setCurrentIndex(-1)
        self.buy_commission_comboBox_2.setCurrentIndex(-1)
        self.sell_commission_comboBox_2.setCurrentIndex(-1)
        self.sell_stop_loss_comboBox_2.setCurrentIndex(-1)
        self.sell_take_profit_comboBox_2.setCurrentIndex(-1)

        self.check_if_disabled_needed_for_settings_fields(
            self.stop_loss_checkbox.isChecked(),
            self.sell_stop_loss_lineEdit_1,
            self.sell_stop_loss_comboBox_2,
            self.label_9)

        self.check_if_disabled_needed_for_settings_fields(
            self.take_profit_checkbox.isChecked(),
            self.sell_take_profit_lineEdit_1,
            self.sell_take_profit_comboBox_2,
            self.label_10)

        # req_exp allows only one '.' in number
        number_regular_expression = QRegExp("^(([1-9][0-9]*)?[0-9](\.[0-9]*)?|\.[0-9]+)$")
        self.buy_commission_lineEdit_1.setValidator(QRegExpValidator(number_regular_expression, self))
        self.buy_balance_lineEdit2.setValidator(QRegExpValidator(number_regular_expression, self))
        self.sell_commission_lineEdit_1.setValidator(QRegExpValidator(number_regular_expression, self))
        self.sell_balance_lineEdit.setValidator(QRegExpValidator(number_regular_expression, self))
        self.sell_stop_loss_lineEdit_1.setValidator(QRegExpValidator(number_regular_expression, self))
        self.sell_take_profit_lineEdit_1.setValidator(QRegExpValidator(number_regular_expression, self))


        # Buy
        self.p2_add_buy_rule.setIcon(QtGui.QIcon('icons/add_icon.png'))
        self.p2_add_buy_rule.setIconSize(QtCore.QSize(28, 28))
        self.p2_add_buy_rule.setToolTip('Add new buy rule')

        self.p2_copy_buy_rule.setIcon(QtGui.QIcon('icons/copy_icon.png'))
        self.p2_copy_buy_rule.setIconSize(QtCore.QSize(28, 28))
        self.p2_copy_buy_rule.clicked.connect(lambda: self.copy_buy_rule())
        self.p2_copy_buy_rule.setToolTip('Copy selected rule')

        self.p2_edit_buy_rule.setIcon(QtGui.QIcon('icons/edit_icon.png'))
        self.p2_edit_buy_rule.setIconSize(QtCore.QSize(28, 28))
        self.p2_edit_buy_rule.setToolTip('Edit selected buy rule')

        self.p2_delete_buy_rule.setIcon(QtGui.QIcon('icons/trash_icon.png'))
        self.p2_delete_buy_rule.setIconSize(QtCore.QSize(28, 28))
        self.p2_delete_buy_rule.clicked.connect(lambda: self.delete_buy_rule())
        self.p2_delete_buy_rule.setToolTip('Remove selected buy rule')

        self.p2_save_strategy_1.setIcon(QtGui.QIcon('icons/save_icon.png'))
        self.p2_save_strategy_1.setIconSize(QtCore.QSize(28, 28))
        self.p2_save_strategy_1.clicked.connect(lambda: self.save_rules_to_json_file())
        self.p2_save_strategy_1.setToolTip('Save buy and sell rules to file')

        self.p2_load_strategy_1.setIcon(QtGui.QIcon('icons/load_icon.png'))
        self.p2_load_strategy_1.setIconSize(QtCore.QSize(28, 28))
        self.p2_load_strategy_1.clicked.connect(lambda: self.load_rules_from_json_file())
        self.p2_load_strategy_1.setToolTip('Load buy and sell rules from file')

        self.p2_plot_indicator_1.setIcon(QtGui.QIcon('icons/plot_icon.png'))
        self.p2_plot_indicator_1.setIconSize(QtCore.QSize(28, 28))
        self.p2_plot_indicator_1.clicked.connect(lambda: self.display_form_to_plot_indicators())
        self.p2_plot_indicator_1.setToolTip('Plot indicator')

        # Sell
        self.p2_add_sell_rule.setIcon(QtGui.QIcon('icons/add_icon.png'))
        self.p2_add_sell_rule.setIconSize(QtCore.QSize(28, 28))
        self.p2_add_sell_rule.setToolTip('Add new sell rule')

        self.p2_copy_sell_rule.setIcon(QtGui.QIcon('icons/copy_icon.png'))
        self.p2_copy_sell_rule.setIconSize(QtCore.QSize(28, 28))
        self.p2_copy_sell_rule.clicked.connect(lambda: self.copy_sell_rule())
        self.p2_copy_sell_rule.setToolTip('Copy selected rule')

        self.p2_edit_sell_rule.setIcon(QtGui.QIcon('icons/edit_icon.png'))
        self.p2_edit_sell_rule.setIconSize(QtCore.QSize(28, 28))
        self.p2_edit_sell_rule.setToolTip('Edit selected sell rule')

        self.p2_delete_sell_rule.setIcon(QtGui.QIcon('icons/trash_icon.png'))
        self.p2_delete_sell_rule.setIconSize(QtCore.QSize(28, 28))
        self.p2_delete_sell_rule.clicked.connect(lambda: self.delete_sell_rule())
        self.p2_delete_sell_rule.setToolTip('Remove selected sell rule')

        self.p2_save_strategy_2.setIcon(QtGui.QIcon('icons/save_icon.png'))
        self.p2_save_strategy_2.setIconSize(QtCore.QSize(28, 28))
        self.p2_save_strategy_2.clicked.connect(lambda: self.save_rules_to_json_file())
        self.p2_save_strategy_2.setToolTip('Save buy and sell rules to file')

        self.p2_load_strategy_2.setIcon(QtGui.QIcon('icons/load_icon.png'))
        self.p2_load_strategy_2.setIconSize(QtCore.QSize(28, 28))
        self.p2_load_strategy_2.clicked.connect(lambda: self.load_rules_from_json_file())
        self.p2_load_strategy_2.setToolTip('Load buy and sell rules from file')

        self.p2_plot_indicator_2.setIcon(QtGui.QIcon('icons/plot_icon.png'))
        self.p2_plot_indicator_2.setIconSize(QtCore.QSize(28, 28))
        self.p2_plot_indicator_2.clicked.connect(lambda: self.display_form_to_plot_indicators())
        self.p2_plot_indicator_2.setToolTip('Plot indicator')


########################################################################################################################

    def display_add_strategy_rule_page_buy_context(self, strategy_page_object):
        self.receive_buy_strategy_rule_to_add_object = Receive_Buy_Strategy_Rule_To_Add()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        list_of_items_in_buy_qtreewidget = \
            self.p2_buyCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
        add_strategy_page_widget.load_qtreewidget(list_of_items_in_buy_qtreewidget)
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(
            lambda: add_strategy_page_widget.add_new_rule(self.receive_buy_strategy_rule_to_add_object,
                                                          strategy_page_object))

    def copy_buy_rule(self):
        if self.p2_buyCondition_treeWidget.selectedItems()[0].parent() is None:
            new_rule = QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget,
                                                 [self.p2_buyCondition_treeWidget.selectedItems()[0].text(0)])
        else:
            new_rule = QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget.selectedItems()[0].parent(),
                                                 [self.p2_buyCondition_treeWidget.selectedItems()[0].text(0)])

        self.copy_all_items_under(self.p2_buyCondition_treeWidget.selectedItems()[0], new_rule)
        self.p2_buyCondition_treeWidget.expandAll()

    def display_add_strategy_rule_page_modify_buy_context(self):
        receive_strategy_rule_to_modify_object = Receive_Strategy_Rule_To_Modify()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        add_strategy_page_widget.load_rule_details_to_modify(self.p2_buyCondition_treeWidget.currentItem().text(0))
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(
            lambda: add_strategy_page_widget.save_modified_rule(self.p2_buyCondition_treeWidget.currentItem(),
                                                                receive_strategy_rule_to_modify_object))

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
            buy_rules['buy_rules'][x]['qTreeWidgetItem_Parent'] = \
                str(buy_rules['buy_rules'][x]['qTreeWidgetItem_Parent'])

        buy_settings = get_buy_simulation_settings(self)
        print(buy_settings)

        # get sell rules and convert qTreeWidgetItems to string
        sell_rules = get_sell_rules(self)
        for x in range(len(sell_rules['sell_rules'])):
            sell_rules['sell_rules'][x]['qTreeWidgetItem'] = str(sell_rules['sell_rules'][x]['qTreeWidgetItem'])
            sell_rules['sell_rules'][x]['qTreeWidgetItem_Parent'] = \
                str(sell_rules['sell_rules'][x]['qTreeWidgetItem_Parent'])

        sell_settings = get_sell_simulation_settings(self)
        print(sell_settings)

        path_to_file = QtWidgets.QFileDialog.getSaveFileName(self,
                                                             'Save strategy to JSON file',
                                                             current_dir[:-6] + '\data\strategy', 'JSON Files (*.json)')

        combined_rules = {'buy_rules': buy_rules['buy_rules'],
                          'buy_settings': buy_settings['buy_settings'],
                          'sell_rules': sell_rules['sell_rules'],
                          'sell_settings': sell_settings['sell_settings']}
        with open(path_to_file[0], 'w') as file:
            json.dump(combined_rules, file, indent=4)

    def display_form_to_plot_indicators(self):
        define_indicator_to_plot_page = Define_Indicator_To_Plot_Page()
        define_indicator_to_plot_page.show()

########################################################################################################################

    def display_add_strategy_rule_page_sell_context(self, strategy_page_object):
        self.receive_sell_strategy_rule_to_add_object = Receive_Sell_Strategy_Rule_To_Add()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        list_of_items_in_sell_qtreewidget = \
            self.p2_sellCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)

        add_strategy_page_widget.load_qtreewidget(list_of_items_in_sell_qtreewidget)
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(
            lambda: add_strategy_page_widget.add_new_rule(self.receive_sell_strategy_rule_to_add_object,
                                                          strategy_page_object))

    def copy_sell_rule(self):
        if self.p2_sellCondition_treeWidget.selectedItems()[0].parent() is None:
            new_rule = QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget,
                                                 [self.p2_sellCondition_treeWidget.selectedItems()[0].text(0)])
        else:
            new_rule = QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget.selectedItems()[0].parent(),
                                                 [self.p2_sellCondition_treeWidget.selectedItems()[0].text(0)])

        self.copy_all_items_under(self.p2_sellCondition_treeWidget.selectedItems()[0], new_rule)
        self.p2_sellCondition_treeWidget.expandAll()

    def display_add_strategy_rule_page_modify_sell_context(self):
        receive_strategy_rule_to_modify_object = Receive_Strategy_Rule_To_Modify()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        add_strategy_page_widget.load_rule_details_to_modify(self.p2_sellCondition_treeWidget.currentItem().text(0))
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(
            lambda: add_strategy_page_widget.save_modified_rule(self.p2_sellCondition_treeWidget.currentItem(),
                                                                receive_strategy_rule_to_modify_object))

    def delete_sell_rule(self):
        print('delete_sell_rule')
        root = self.p2_sellCondition_treeWidget.invisibleRootItem()
        for item in self.p2_sellCondition_treeWidget.selectedItems():
            (item.parent() or root).removeChild(item)

    def load_rules_from_json_file(self):
        path_to_json_file = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                  'Load strategy from JSON file',
                                                                  current_dir[:-6] + '\data\strategy',
                                                                  'JSON Files (*.json)')
        with open(path_to_json_file[0]) as json_file:
            loaded_rules = json.load(json_file)

        # clear both QTreeWidgets
        self.p2_buyCondition_treeWidget.clear()
        self.p2_sellCondition_treeWidget.clear()
        buy_rules = loaded_rules['buy_rules']
        buy_settings = loaded_rules['buy_settings'][0]
        sell_rules = loaded_rules['sell_rules']
        sell_settings = loaded_rules['sell_settings'][0]
        QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget, [buy_rules[0]['rule_text']])
        for x in range(len(buy_rules)-1):
            for y in range(len(buy_rules)):
                if buy_rules[x+1]['qTreeWidgetItem_Parent'] == buy_rules[y]['qTreeWidgetItem']:
                    found_parent = buy_rules[y]['rule_text']
            QtWidgets.QTreeWidgetItem(self.p2_buyCondition_treeWidget
                                      .findItems(found_parent,
                                                QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)[-1],
                                                [buy_rules[x+1]['rule_text']])

        self.buy_price_source_comboBox.setCurrentIndex(self.buy_price_source_comboBox.
                                                       findText(buy_settings['price_source'], QtCore.Qt.MatchContains))
        self.buy_commission_lineEdit_1.setText(buy_settings['fee'])
        self.buy_commission_comboBox_2.setCurrentIndex(self.buy_commission_comboBox_2.
                                                       findText(buy_settings['fee_unit'], QtCore.Qt.MatchContains))
        self.buy_balance_lineEdit2.setText(buy_settings['starting_balance'])

        QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget, [sell_rules[0]['rule_text']])
        for x in range(len(sell_rules)-1):
            for y in range(len(sell_rules)):
                if sell_rules[x+1]['qTreeWidgetItem_Parent'] == sell_rules[y]['qTreeWidgetItem']:
                    found_parent = sell_rules[y]['rule_text']
            QtWidgets.QTreeWidgetItem(self.p2_sellCondition_treeWidget
                                      .findItems(found_parent,
                                                 QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)[-1],
                                                 [sell_rules[x+1]['rule_text']])

        self.sell_price_source_comboBox.setCurrentIndex(self.sell_price_source_comboBox
                                                        .findText(sell_settings['price_source'],
                                                                  QtCore.Qt.MatchContains))
        self.sell_commission_lineEdit_1.setText(sell_settings['fee'])
        self.sell_commission_comboBox_2.setCurrentIndex(self.sell_commission_comboBox_2
                                                        .findText(sell_settings['fee_unit'],
                                                                  QtCore.Qt.MatchContains))
        self.sell_balance_lineEdit.setText(sell_settings['starting_balance'])

        self.check_if_disabled_needed_for_settings_fields(self.stop_loss_checkbox.isChecked(),
                                                          self.sell_stop_loss_lineEdit_1,
                                                          self.sell_stop_loss_comboBox_2,
                                                          self.label_9)

        self.check_if_disabled_needed_for_settings_fields(self.take_profit_checkbox.isChecked(),
                                                          self.sell_take_profit_lineEdit_1,
                                                          self.sell_take_profit_comboBox_2,
                                                          self.label_10)


        if sell_settings['is_stop_loss_selected']:
            self.stop_loss_checkbox.setChecked(True)
            self.sell_stop_loss_lineEdit_1.setText(sell_settings['stop_loss'])
            self.sell_stop_loss_comboBox_2.setCurrentIndex(self.sell_stop_loss_comboBox_2
                                                           .findText(sell_settings['stop_loss_unit'],
                                                                     QtCore.Qt.MatchContains))
        else:
            self.stop_loss_checkbox.setChecked(False)
            self.sell_stop_loss_lineEdit_1.setText('')
            self.sell_stop_loss_comboBox_2.setCurrentIndex(-1)

        if sell_settings['is_take_profit_selected']:
            self.take_profit_checkbox.setChecked(True)
            self.sell_take_profit_lineEdit_1.setText(sell_settings['take_profit'])
            self.sell_take_profit_comboBox_2.setCurrentIndex(self.sell_take_profit_comboBox_2
                                                             .findText(sell_settings['take_profit_unit'],
                                                                       QtCore.Qt.MatchContains))
        else:
            self.take_profit_checkbox.setChecked(False)
            self.sell_take_profit_lineEdit_1.setText('')
            self.sell_take_profit_comboBox_2.setCurrentIndex(-1)

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


    def check_if_all_fileds_have_values(self):
        list_of_fields = [self.buy_price_source_comboBox, self.buy_commission_lineEdit_1, self.buy_commission_comboBox_2,
                          self.buy_balance_lineEdit2, self.sell_price_source_comboBox, self.sell_commission_lineEdit_1,
                          self.sell_commission_comboBox_2, self.sell_balance_lineEdit,
                          self.p2_buyCondition_treeWidget, self.p2_sellCondition_treeWidget]
        
        if self.stop_loss_checkbox.isChecked():
            list_of_fields.append(self.sell_stop_loss_lineEdit_1)
            list_of_fields.append(self.sell_stop_loss_comboBox_2)
        else:
            self.sell_stop_loss_lineEdit_1.setProperty('invalid', False)
            self.sell_stop_loss_lineEdit_1.style().polish(self.sell_stop_loss_lineEdit_1)
            self.sell_stop_loss_comboBox_2.setProperty('invalid', False)
            self.sell_stop_loss_comboBox_2.style().polish(self.sell_stop_loss_comboBox_2)

        if self.take_profit_checkbox.isChecked():
            list_of_fields.append(self.sell_take_profit_lineEdit_1)
            list_of_fields.append(self.sell_take_profit_comboBox_2)
        else:
            self.sell_take_profit_lineEdit_1.setProperty('invalid', False)
            self.sell_take_profit_lineEdit_1.style().polish(self.sell_take_profit_lineEdit_1)
            self.sell_take_profit_comboBox_2.setProperty('invalid', False)
            self.sell_take_profit_comboBox_2.style().polish(self.sell_take_profit_comboBox_2)

        if False in check_if_all_fields_have_text(list_of_fields):
            show_error_message(self.error_message_label, 'Please provide input into highlighted fields.')
            return False
        else:
            hide_error_message(self.error_message_label)
            return True

    def copy_all_items_under(self, original_rule, new_added_rule):
        if original_rule.child(0) is not None:
            for x in range(original_rule.childCount()):
                QtWidgets.QTreeWidgetItem(new_added_rule, [original_rule.child(x).text(0)])
                self.copy_all_items_under(original_rule.child(x), new_added_rule.child(x))

########################################################################################################################
    def check_if_disabled_needed_for_settings_fields(self, is_checked, value_line_edit, unit_dropdown, label):
        if is_checked:
            value_line_edit.setReadOnly(False)
            value_line_edit.setCursor(QtCore.Qt.IBeamCursor)
            unit_dropdown.setEnabled(True)
            unit_dropdown.setCursor(QtCore.Qt.ArrowCursor)
            label.setStyleSheet('color: rgb(255, 255, 255);')
        else:
            value_line_edit.setReadOnly(True)
            value_line_edit.setCursor(QtCore.Qt.ForbiddenCursor)
            value_line_edit.setText('')
            value_line_edit.setProperty('invalid', False)
            value_line_edit.style().polish(value_line_edit)
            unit_dropdown.setEnabled(False)
            unit_dropdown.setCursor(QtCore.Qt.ForbiddenCursor)
            unit_dropdown.setCurrentIndex(-1)
            unit_dropdown.setProperty('invalid', False)
            unit_dropdown.style().polish(unit_dropdown)
            label.setStyleSheet('color: rgb(80,80,80);')


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