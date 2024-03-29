import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtCore import Signal
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator
from utilities.helpers import indicator_options_name, show_error_message, hide_error_message, \
    check_if_all_fields_have_text


current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/change_indicator_form_page.ui"))


class Change_Indicator_Form_Page(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        self.cancel_button.clicked.connect(lambda: self.close_window())
        hide_error_message(self.error_message_label)


    def set_up_view(self, indicator, typed_options, qlineedit_field, recive_indicator_options_object):
        #set up validator for input fields
        if indicator == 'SAR (Stop and Reverse)':
            number_regular_expression = QRegExp('^[0][.][0-9]{0,5}$')
        elif indicator == 'Value (Plain integer or double)':
            number_regular_expression = QRegExp('')
        else:
            number_regular_expression = QRegExp('^(0|[1-9][0-9]{0,9})$')

        number_regular_expression_validator = QRegExpValidator(number_regular_expression, self)
        self.lineEdit_1.setValidator(number_regular_expression_validator)
        self.lineEdit_2.setValidator(number_regular_expression_validator)
        self.lineEdit_3.setValidator(number_regular_expression_validator)
        self.lineEdit_4.setValidator(number_regular_expression_validator)

        typed_options = typed_options[1:-1]
        typed_options_list = []
        coma_count = typed_options.count(',')
        if coma_count == 0:
            typed_options_list.append(typed_options)
        else:
            for coma in range(coma_count):
                typed_options_list.append(typed_options[:typed_options.find(',')])
                typed_options = typed_options[typed_options.find(',') + 2:]
                if coma == coma_count - 1:
                    typed_options_list.append(typed_options)

        fields = [[self.label_1, self.lineEdit_1], [self.label_2, self.lineEdit_2],
                  [self.label_3, self.lineEdit_3], [self.label_4, self.lineEdit_4],[self.label_5, self.comboBox]]
        list_of_options_name = indicator_options_name.get(indicator)
        if list_of_options_name[-1] == 'Source':
            for x in range(len(list_of_options_name)-1):
                fields[x][0].setText(list_of_options_name[x])
                fields[x][1].setText(typed_options_list[x])
            self.label_5.setText(list_of_options_name[-1])
            self.comboBox.setCurrentIndex(self.comboBox.findText(typed_options_list[-1], QtCore.Qt.MatchContains))
        else:
            for x in range(len(list_of_options_name)):
                fields[x][0].setText(list_of_options_name[x])
                fields[x][1].setText(typed_options_list[x])

        for x in fields:
            if x[0].text() == 'TextLabel':
                x[0].hide()
                x[1].hide()

        self.addRule_button.clicked.connect(
            lambda: self.save_indicator_options(qlineedit_field, recive_indicator_options_object))


    def save_indicator_options(self, qlineedit_field, recive_indicator_options_object):
        string_with_formatted_options = '('

        list_of_fields = [self.lineEdit_1, self.lineEdit_2, self.lineEdit_3, self.lineEdit_4, self.comboBox]
        list_of_fields_status = []

        for x in list_of_fields:
            if isinstance(x, QtWidgets.QLineEdit):
                if x.isVisible():
                    if x.text():
                        x.setProperty('invalid', False)
                        x.style().polish(x)
                        list_of_fields_status.append(True)
                        string_with_formatted_options += x.text().strip() + ', '
                    else:
                        x.setProperty('invalid', True)
                        x.style().polish(x)
                        list_of_fields_status.append(False)
            elif isinstance(x, QtWidgets.QComboBox):
                if x.isVisible():
                    if x.currentText():
                        x.setProperty('invalid', False)
                        x.style().polish(x)
                        list_of_fields_status.append(True)
                        string_with_formatted_options += x.currentText().strip()
                    else:
                        x.setProperty('invalid', True)
                        x.style().polish(x)
                        list_of_fields_status.append(False)
                else:
                    string_with_formatted_options = string_with_formatted_options[:-2]

        if False in list_of_fields_status:
            show_error_message(self.error_message_label, 'Fields cannot be empty.')
            return False

        string_with_formatted_options += ')'
        self.close_window()
        sender = Send_Indicator_Option()
        sender.send_indicator_option(string_with_formatted_options, qlineedit_field, recive_indicator_options_object)

    def close_window(self):
        self.close()

class Send_Indicator_Option(QtCore.QObject):
    signal = Signal()
    def send_indicator_option(self, indicator_option, qlineedit_field, recive_indicator_options_object):
        self.signal.connect(
            lambda: recive_indicator_options_object.recive_indicator_options(indicator_option,qlineedit_field))
        self.signal.emit()

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = Change_Indicator_Form_Page()
    w.show()
    sys.exit(app.exec_())