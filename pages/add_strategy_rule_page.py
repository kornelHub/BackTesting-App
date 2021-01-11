import os
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtUiTools import loadUiType
from PySide2.QtCore import Signal
from helpers import add_strategy_button_style_sheet_normal, add_strategy_button_style_sheet_clicked, \
    indicator_default_options

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/add_strategy_rule_page.ui"))


class Add_Strategy_Rule_Widget(Form, Base):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        self.p3_cancel_button.clicked.connect(lambda: self.close())
        self.add_strategy_rule_treeWidget.setHeaderLabel("")
        self.p3_firstIndicatorOptions_lineEdit_1.setText(indicator_default_options.get('SMA (Simple Moving Average)'))
        self.p3_firstIndicatorOptions_lineEdit_2.setText('[0]')
        self.p3_secondIndicatorOptions_lineEdit_1.setText(indicator_default_options.get('SMA (Simple Moving Average)'))
        self.p3_secondIndicatorOptions_lineEdit_2.setText('[0]')
        self.list_of_parent_text = []
        self.current_selected_math_char = ''

        self.selectMathChar_Button_1.clicked.connect(lambda: self.math_char_buttons_behavior(self.selectMathChar_Button_1))
        self.selectMathChar_Button_2.clicked.connect(lambda: self.math_char_buttons_behavior(self.selectMathChar_Button_2))
        self.selectMathChar_Button_3.clicked.connect(lambda: self.math_char_buttons_behavior(self.selectMathChar_Button_3))
        self.selectMathChar_Button_4.clicked.connect(lambda: self.math_char_buttons_behavior(self.selectMathChar_Button_4))
        self.selectMathChar_Button_5.clicked.connect(lambda: self.math_char_buttons_behavior(self.selectMathChar_Button_5))

        self.p3_firstIndicator_comboBox.currentIndexChanged.connect(lambda: self.autofill_indicator_option(self.p3_firstIndicator_comboBox,self.p3_firstIndicatorOptions_lineEdit_1))

        self.p3_sedondIndicator_comboBox.currentIndexChanged.connect(lambda: self.autofill_indicator_option(self.p3_sedondIndicator_comboBox,self.p3_secondIndicatorOptions_lineEdit_1))

    def autofill_indicator_option(self, combo_box, linked_line_edit):
        linked_line_edit.setText(indicator_default_options.get(combo_box.currentText()))

    def math_char_buttons_behavior(self, clicked_button):
        buttons = [self.selectMathChar_Button_1, self.selectMathChar_Button_2, self.selectMathChar_Button_3, self.selectMathChar_Button_4, self.selectMathChar_Button_5]
        clicked_button.setStyleSheet(add_strategy_button_style_sheet_clicked)
        self.current_selected_math_char = clicked_button.text()
        buttons.remove(clicked_button)
        for item in buttons:
            item.setStyleSheet(add_strategy_button_style_sheet_normal)

    def load_qtreewidget(self, list_of_objects):
        for element in list_of_objects:
            if element.parent() is None:
                # Add item to qTreeWidget and make is checkable
                QtWidgets.QTreeWidgetItem(self.add_strategy_rule_treeWidget, [element.text(0)]).setCheckState(0, QtCore.Qt.Unchecked)
            else:
                parent_of_current_element = self.add_strategy_rule_treeWidget.findItems(element.parent().text(0), QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
                # Add item to qTreeWidget and make is checkable
                QtWidgets.QTreeWidgetItem(parent_of_current_element[0], [element.text(0)]).setCheckState(0, QtCore.Qt.Unchecked)
        self.add_strategy_rule_treeWidget.expandAll()

    def add_rule(self, receive_strategy_rule_object):
        new_rule_to_add = self.p3_firstIndicator_comboBox.currentText()[:self.p3_firstIndicator_comboBox.currentText().find("(")-1] + ' ' + self.p3_firstIndicatorOptions_lineEdit_1.text() + ' ' + self.p3_firstIndicatorOptions_lineEdit_2.text() \
                          + ' ' + self.current_selected_math_char \
                          + ' ' + self.p3_sedondIndicator_comboBox.currentText()[:self.p3_sedondIndicator_comboBox.currentText().find("(")-1] + ' ' + self.p3_secondIndicatorOptions_lineEdit_1.text() + ' ' + self.p3_secondIndicatorOptions_lineEdit_2.text()

        # loops through  all items, if item is checked > get text of all parents
        for item in self.add_strategy_rule_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0):
            if (item.checkState(0) > 0):
                self.create_list_of_parents_text(item, [])

        print(new_rule_to_add)
        sender = Send_Strategy_Rule()
        sender.on_send(new_rule_to_add, self.list_of_parent_text, receive_strategy_rule_object)
        self.close()

    def create_list_of_parents_text(self, qTreeWidgetItem, helper_list):
        if qTreeWidgetItem.parent() is None:
            helper_list.append(qTreeWidgetItem.text(0))
            self.list_of_parent_text.append(helper_list)
            return True
        else:
            helper_list.append(qTreeWidgetItem.text(0))
            self.create_list_of_parents_text(qTreeWidgetItem.parent(), helper_list)

    def load_rule_details_to_modify(self, rule_to_modify):
        first_indicator_short_name = rule_to_modify[:rule_to_modify.find('(')-1]
        rule_to_modify = rule_to_modify[rule_to_modify.find('('):]
        first_indicator_options = rule_to_modify[:rule_to_modify.find('[')-1]
        rule_to_modify = rule_to_modify[rule_to_modify.find('['):]
        first_indicator_period = rule_to_modify[:rule_to_modify.find(']')+1]
        rule_to_modify = rule_to_modify[rule_to_modify.find(']')+2:]
        math_char = rule_to_modify[:2].strip()
        rule_to_modify = rule_to_modify[2:].strip()
        second_indicator_short_name = rule_to_modify[:rule_to_modify.find('(') - 1]
        rule_to_modify = rule_to_modify[rule_to_modify.find('('):]
        second_indicator_options = rule_to_modify[:rule_to_modify.find('[') - 1]
        rule_to_modify = rule_to_modify[rule_to_modify.find('['):]
        second_indicator_period = rule_to_modify

        self.p3_firstIndicator_comboBox.setCurrentIndex(self.p3_firstIndicator_comboBox.findText(first_indicator_short_name, QtCore.Qt.MatchContains))
        self.p3_firstIndicatorOptions_lineEdit_1.setText(first_indicator_options)
        self.p3_firstIndicatorOptions_lineEdit_2.setText(first_indicator_period)
        buttons = [self.selectMathChar_Button_1, self.selectMathChar_Button_2, self.selectMathChar_Button_3, self.selectMathChar_Button_4, self.selectMathChar_Button_5]
        for button in buttons:
            if button.text() == math_char:
                self.current_selected_math_char = math_char
                button.setStyleSheet(add_strategy_button_style_sheet_clicked)
        self.p3_sedondIndicator_comboBox.setCurrentIndex(self.p3_sedondIndicator_comboBox.findText(second_indicator_short_name, QtCore.Qt.MatchContains))
        self.p3_secondIndicatorOptions_lineEdit_1.setText(second_indicator_options)
        self.p3_secondIndicatorOptions_lineEdit_2.setText(second_indicator_period)

class Send_Strategy_Rule(QtCore.QObject):
    signal = Signal()

    def on_send(self, new_rule_to_add, text_of_parent_element, reciver):
        self.signal.connect(lambda: reciver.on_recive(new_rule_to_add, text_of_parent_element))
        self.signal.emit()


if __name__ == '__add_strategy_rule_page__':
    import sys

    app = QtGui.QGuiApplication(sys.argv)
    w = Add_Strategy_Rule_Widget()
    w.show()
    sys.exit(app.exec_())
