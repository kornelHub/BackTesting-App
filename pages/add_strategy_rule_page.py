import os
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtUiTools import loadUiType
from PySide2.QtCore import Signal, Slot
from utilities.helpers import add_strategy_button_style_sheet_normal, add_strategy_button_style_sheet_clicked, \
    indicator_default_options
from pages.change_indicator_form_page import Change_Indicator_Form_Page

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
        self.p3_firstIndicatorOptions_button_1.setText(indicator_default_options.get('SMA (Simple Moving Average)'))
        self.p3_firstIndicatorOptions_comboBox_2.setCurrentIndex(0)
        self.p3_secondIndicatorOptions_button_1.setText(indicator_default_options.get('SMA (Simple Moving Average)'))
        self.p3_secondIndicatorOptions_comboBox_2.setCurrentIndex(1)
        self.list_of_parent_text = []
        self.current_selected_math_char = ''
        self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False)

        self.selectMathChar_Button_1.clicked.connect(lambda: self.math_char_buttons_behavior(self.selectMathChar_Button_1))
        self.selectMathChar_Button_2.clicked.connect(lambda: self.math_char_buttons_behavior(self.selectMathChar_Button_2))
        self.selectMathChar_Button_3.clicked.connect(lambda: self.math_char_buttons_behavior(self.selectMathChar_Button_3))
        self.selectMathChar_Button_4.clicked.connect(lambda: self.math_char_buttons_behavior(self.selectMathChar_Button_4))
        self.selectMathChar_Button_5.clicked.connect(lambda: self.math_char_buttons_behavior(self.selectMathChar_Button_5))

        self.p3_firstIndicator_comboBox.currentIndexChanged.connect(lambda: self.autofill_indicator_option(self.p3_firstIndicator_comboBox, self.p3_firstIndicatorOptions_button_1, self.p3_firstIndicatorOptions_comboBox_2, self.label_4))
        self.p3_sedondIndicator_comboBox.currentIndexChanged.connect(lambda: self.autofill_indicator_option(self.p3_sedondIndicator_comboBox, self.p3_secondIndicatorOptions_button_1, self.p3_secondIndicatorOptions_comboBox_2, self.label_7))

        self.p3_firstIndicatorOptions_button_1.clicked.connect(lambda: self.open_form_with_indicator_options(self.p3_firstIndicator_comboBox.currentText(), self.p3_firstIndicatorOptions_button_1.text(), self.p3_firstIndicatorOptions_button_1))
        self.p3_secondIndicatorOptions_button_1.clicked.connect(lambda: self.open_form_with_indicator_options(self.p3_sedondIndicator_comboBox.currentText(), self.p3_secondIndicatorOptions_button_1.text(), self.p3_secondIndicatorOptions_button_1))

    def autofill_indicator_option(self, combo_box, linked_option_edit, linked_period_edit, linked_label):
        if combo_box.currentText() == "Value (Plain integer or double)":
            linked_period_edit.setEnabled(False)
            linked_period_edit.setCurrentIndex(0)
            linked_label.setText('Value:')
            linked_option_edit.setText(indicator_default_options.get(combo_box.currentText()))
        elif combo_box.currentText() == 'Open (Open price of candle)' \
                or combo_box.currentText() == 'High (High price of candle)' \
                or combo_box.currentText() == 'Low (Low price of candle)' \
                or combo_box.currentText() == 'Close (Close price of candle)'\
                or combo_box.currentText() == 'Volume (Amount traded in amount of time)':
            linked_option_edit.setText(indicator_default_options.get(combo_box.currentText()))
            linked_period_edit.setCurrentIndex(0)
            linked_label.setText('Value:')
        else:
            linked_label.setText('Options:')
            linked_option_edit.setText(indicator_default_options.get(combo_box.currentText()))
            linked_period_edit.setEnabled(True)

        if indicator_default_options.get(combo_box.currentText()) == '(-)':
            linked_option_edit.setEnabled(False)
        else:
            linked_option_edit.setEnabled(True)

    def math_char_buttons_behavior(self, clicked_button):
        buttons = [self.selectMathChar_Button_1, self.selectMathChar_Button_2, self.selectMathChar_Button_3, self.selectMathChar_Button_4, self.selectMathChar_Button_5]
        clicked_button.setStyleSheet(add_strategy_button_style_sheet_clicked)
        self.current_selected_math_char = clicked_button.text()
        buttons.remove(clicked_button)
        for item in buttons:
            item.setStyleSheet(add_strategy_button_style_sheet_normal)

    def get_and_combine_text_from_fields(self):
        new_rule_to_add = self.p3_firstIndicator_comboBox.currentText()[:self.p3_firstIndicator_comboBox.currentText().find("(")-1] + ' ' + self.p3_firstIndicatorOptions_button_1.text() + ' ' + self.p3_firstIndicatorOptions_comboBox_2.currentText() \
                          + ' ' + self.current_selected_math_char \
                          + ' ' + self.p3_sedondIndicator_comboBox.currentText()[:self.p3_sedondIndicator_comboBox.currentText().find("(")-1] + ' ' + self.p3_secondIndicatorOptions_button_1.text() + ' ' + self.p3_secondIndicatorOptions_comboBox_2.currentText()
        return new_rule_to_add

    ### function responsible for adding new strategy rule
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

    def create_list_of_parents_text(self, qTreeWidgetItem, helper_list):
        if qTreeWidgetItem.parent() is None:
            helper_list.append(qTreeWidgetItem.text(0))
            self.list_of_parent_text.append(helper_list)
            return True
        else:
            helper_list.append(qTreeWidgetItem.text(0))
            self.create_list_of_parents_text(qTreeWidgetItem.parent(), helper_list)

    def add_new_rule(self, receiver_object, strategy_page_object):
        print(self)
        new_rule_to_add = self.get_and_combine_text_from_fields()
        # loops through  all items, if item is checked > get text of all parents
        for item in self.add_strategy_rule_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0):
            if (item.checkState(0) > 0):
                self.create_list_of_parents_text(item, [])

        print('New rule to add: ', new_rule_to_add)
        sender = Send_Strategy_Rule_To_Add()
        sender.send_rule_to_add(new_rule_to_add, self.list_of_parent_text, receiver_object, strategy_page_object)
        self.close()

    ### function responsible for modyfing rule
    def load_rule_details_to_modify(self, rule_to_modify):
        self.tree_widget.hide()
        self.label.setText('Modify rule')
        w = self.size().width()
        h = self.size().height()
        self.resize(w, h/2)
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
        self.p3_firstIndicatorOptions_button_1.setText(first_indicator_options)
        self.p3_firstIndicatorOptions_comboBox_2.setCurrentIndex(self.p3_firstIndicatorOptions_comboBox_2.findText(first_indicator_period, QtCore.Qt.MatchContains))
        buttons = [self.selectMathChar_Button_1, self.selectMathChar_Button_2, self.selectMathChar_Button_3, self.selectMathChar_Button_4, self.selectMathChar_Button_5]
        for button in buttons:
            if button.text() == math_char:
                self.current_selected_math_char = math_char
                button.setStyleSheet(add_strategy_button_style_sheet_clicked)
        self.p3_sedondIndicator_comboBox.setCurrentIndex(self.p3_sedondIndicator_comboBox.findText(second_indicator_short_name, QtCore.Qt.MatchContains))
        self.p3_secondIndicatorOptions_button_1.setText(second_indicator_options)
        self.p3_secondIndicatorOptions_comboBox_2.setCurrentIndex(self.p3_secondIndicatorOptions_comboBox_2.findText(second_indicator_period, QtCore.Qt.MatchContains))

    def save_modified_rule(self, current_selected_item, receiver_object):
        rule_to_modify = self.get_and_combine_text_from_fields()
        print('Rule to modify: ', rule_to_modify)
        sender = Send_Strategy_Rule_To_Modify()
        sender.send_rule_to_modify(rule_to_modify, current_selected_item, receiver_object)
        self.close()

    def open_form_with_indicator_options(self, indicator, typed_options, qlineedit_field):
        recive_indicator_options_object = Recive_Indicator_Options()
        change_indicator_form_page = Change_Indicator_Form_Page()
        change_indicator_form_page.set_up_view(indicator, typed_options, qlineedit_field, recive_indicator_options_object)
        change_indicator_form_page.show()

class Send_Strategy_Rule_To_Add(QtCore.QObject):
    signal = Signal()
    def send_rule_to_add(self, new_rule_to_add, text_of_parent_element, receiver_object, strategy_page_object):
        self.signal.connect(lambda: receiver_object.receive_and_add_rule(new_rule_to_add, text_of_parent_element, strategy_page_object))
        self.signal.emit()

class Send_Strategy_Rule_To_Modify(QtCore.QObject):
    signal = Signal()
    def send_rule_to_modify(self, rule_to_modify, current_selected_item, receiver_object):
        self.signal.connect(lambda: receiver_object.receive_and_modify_rule(rule_to_modify, current_selected_item))
        self.signal.emit()

class Recive_Indicator_Options(QtCore.QObject):
    @Slot(str)
    def recive_indicator_options(self, indicator_option, qlineedit_field):
        qlineedit_field.setText(indicator_option)

if __name__ == '__add_strategy_rule_page__':
    import sys
    app = QtGui.QGuiApplication(sys.argv)
    w = Add_Strategy_Rule_Widget()
    w.show()
    sys.exit(app.exec_())