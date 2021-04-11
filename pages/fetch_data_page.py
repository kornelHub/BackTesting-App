import os
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtCore import QRegExp
from PySide2.QtGui import QRegExpValidator
from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QFileDialog
from binance.helpers import date_to_milliseconds
from binance_api import fetch_data
from utilities.plot_data import plot_ohlcv_data
import utilities.helpers as helpers


current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/fetch_data_page.ui"))

class Fetch_Data_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.p1_ohlcvPlot_qWebEngineView.hide()

        completer = QtWidgets.QCompleter(helpers.cryptocurrency_pair_dict.keys())
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        completer.popup().setStyleSheet("background-color: rgb(55, 55, 55); font: 10pt 'MS Shell Dlg 2';  color: rgb(255, 255, 255);")
        self.p1_cryptoSymbol_textField.setCompleter(completer)

        # allow number in range 1-31 included, in format 5 or 05
        day_regular_expression = QRegExp("[1-9]|0[0-9]|[12][0-9]|3[01]")
        self.p1_startDate_textField_day.setValidator(QRegExpValidator(day_regular_expression, self))
        self.p1_endDate_textField_day.setValidator(QRegExpValidator(day_regular_expression, self))

        # allow number in range 0-23 included, in format 5 or 05
        hour_regular_expression = QRegExp("[0-9]|0[0-9]|1[0-9]|2[0-3]")
        self.p1_startDate_textField_hour.setValidator(QRegExpValidator(hour_regular_expression, self))
        self.p1_endDate_textField_hour.setValidator(QRegExpValidator(hour_regular_expression, self))

        # allow number in range 0-59  included, in format 5 or 05
        minute_or_second_regular_expression = QRegExp("[0-9]|0[0-9]|[1-5][0-9]")
        self.p1_startDate_textField_minute.setValidator(QRegExpValidator(minute_or_second_regular_expression, self))
        self.p1_startDate_textField_second.setValidator(QRegExpValidator(minute_or_second_regular_expression, self))
        self.p1_endDate_textField_minute.setValidator(QRegExpValidator(minute_or_second_regular_expression, self))
        self.p1_endDate_textField_second.setValidator(QRegExpValidator(minute_or_second_regular_expression, self))

        # allow number in range 2018-2029 included
        year_regular_expression = QRegExp("[2][0](1[8-9]|2[0-9])")
        self.p1_startDate_textField_year.setValidator(QRegExpValidator(year_regular_expression, self))
        self.p1_endDate_textField_year.setValidator(QRegExpValidator(year_regular_expression, self))

        self.list_of_fields = [self.p1_interval_dropdown, self.p1_cryptoSymbol_textField,
                          self.p1_startDate_textField_day, self.p1_startDate_comboBox_month,
                          self.p1_startDate_textField_year, self.p1_startDate_textField_hour,
                          self.p1_startDate_textField_minute, self.p1_startDate_textField_second,
                          self.p1_endDate_textField_day, self.p1_endDate_comboBox_month,
                          self.p1_endDate_textField_year, self.p1_endDate_textField_hour,
                          self.p1_endDate_textField_minute, self.p1_endDate_textField_second]

        self.hide_error_message()


    def hide_error_message(self):
        self.error_message_label.hide()

    def show_error_message(self, message_text):
        self.error_message_label.show()
        self.error_message_label.setText(message_text)


    def check_if_all_fileds_have_values(self):
        is_field_contain_text =[]
        for field in self.list_of_fields:
            if isinstance(field, QtWidgets.QLineEdit):
                if field.text():
                    field.setProperty("invalid", False)
                    field.style().polish(field)
                    is_field_contain_text.append(True)
                else:
                    field.setProperty("invalid", True)
                    field.style().polish(field)
                    is_field_contain_text.append(False)
            elif isinstance(field, QtWidgets.QComboBox):
                if field.currentText():
                    field.setProperty("invalid", False)
                    field.style().polish(field)
                    is_field_contain_text.append(True)
                else:
                    field.setProperty("invalid", True)
                    field.style().polish(field)
                    is_field_contain_text.append(False)

        if False in is_field_contain_text:
            return False
        else:
            return True


    def fetch_data_btn_clicked(self, main_widget_object, path_to_project):
        # returns False if one or more fields are empty
        if not self.check_if_all_fileds_have_values():
            self.show_error_message("Fields cannot be empty.")
            return False

        start_date = self.p1_startDate_textField_day.text() + ' ' + self.p1_startDate_comboBox_month.currentText() \
                     + ' ' + self.p1_startDate_textField_year.text() + ' ' + self.p1_startDate_textField_hour.text() \
                     + ':' + self.p1_startDate_textField_minute.text() + ':' + self.p1_startDate_textField_second.text()
        end_date = self.p1_endDate_textField_day.text() + ' ' + self.p1_endDate_comboBox_month.currentText() \
                   + ' ' + self.p1_endDate_textField_year.text() + ' ' + self.p1_endDate_textField_hour.text() \
                   + ':' + self.p1_endDate_textField_minute.text() + ':' + self.p1_endDate_textField_second.text()

        # return False if From date is bigger that To date
        if int(date_to_milliseconds(start_date)) >= int(date_to_milliseconds(end_date)):
            self.show_error_message("'From' data cannot be bigger that 'To' date")
            print(self.list_of_fields[8:])
            for field in self.list_of_fields[8:]:
                field.setProperty("invalid", True)
                field.style().polish(field)

            return False

        currency_symbol = self.p1_cryptoSymbol_textField.text()
        interval = self.p1_interval_dropdown.currentText()
        path_to_file = QFileDialog.getSaveFileName(self,
                                                   'Save OHLCV data to CSV file',
                                                   path_to_project + '\data', 'Text Files (*.csv)')

        # if user click cancel on dialog window, return False and prevent program from crash
        if not path_to_file[0]:
            return False

        fetch_data.create_csv_with_ohlcv_data(start_time=int(date_to_milliseconds(start_date)),
                                              end_time=int(date_to_milliseconds(end_date)),
                                              currency_pair_symbol=currency_symbol,
                                              interval=interval, path_to_file=path_to_file[0])
        main_widget_object.data_path.setText(path_to_file[0])
        helpers.path_to_csv_file = path_to_file[0]
        self.p1_ohlcvPlot_qWebEngineView.show()
        self.p1_ohlcvPlot_qWebEngineView.setHtml(plot_ohlcv_data(helpers.load_ohlcv_data_from_csv_file()))
        self.hide_error_message()


    def plot_and_autofill_loaded_data(self):
        # if user enter invalid data and try to save, fields become red. Loading data should remove red borders.
        for field in self.list_of_fields:
            field.setProperty("invalid", False)
            field.style().polish(field)

        new_data = helpers.load_ohlcv_data_from_csv_file()
        self.p1_ohlcvPlot_qWebEngineView.show()
        self.p1_ohlcvPlot_qWebEngineView.setHtml(plot_ohlcv_data(new_data))

        currency_pair_symbol = (open(helpers.path_to_csv_file).readline()).rstrip("\n")
        self.p1_cryptoSymbol_textField.setText(currency_pair_symbol)
        start_time = str(helpers.convert_milliseconds_to_date(new_data.iloc[0]['Opentime']))
        end_time = str(helpers.convert_milliseconds_to_date(new_data.iloc[-1]['Opentime']))

        self.p1_interval_dropdown.setCurrentIndex(self.p1_interval_dropdown.findText(helpers.difference_period_dictionary.get(int(new_data.iloc[1]['Opentime'] - new_data.iloc[0]['Opentime'])), QtCore.Qt.MatchContains))

        self.p1_startDate_textField_day.setText(start_time[8:10])
        self.p1_startDate_comboBox_month.setCurrentIndex(self.p1_startDate_comboBox_month.findText(helpers.month_dictionary.get(start_time[5:7]), QtCore.Qt.MatchContains))
        self.p1_startDate_textField_year.setText(start_time[0:4])
        self.p1_startDate_textField_hour.setText(start_time[11:13])
        self.p1_startDate_textField_minute.setText(start_time[14:16])
        self.p1_startDate_textField_second.setText(start_time[17:19])

        self.p1_endDate_textField_day.setText(end_time[8:10])
        self.p1_endDate_comboBox_month.setCurrentIndex(self.p1_endDate_comboBox_month.findText(helpers.month_dictionary.get(end_time[5:7]), QtCore.Qt.MatchContains))
        self.p1_endDate_textField_year.setText(end_time[0:4])
        self.p1_endDate_textField_hour.setText(end_time[11:13])
        self.p1_endDate_textField_minute.setText(end_time[14:16])
        self.p1_endDate_textField_second.setText(end_time[17:19])
        self.hide_error_message()


if __name__ == '__fetch_data_page__':
    import sys
    app = QtGui.QGuiApplication(sys.argv)
    w = Fetch_Data_Widget()
    w.show()
    sys.exit(app.exec_())