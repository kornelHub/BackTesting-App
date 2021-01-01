import os
from PySide2 import QtGui, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QFileDialog
from binance.helpers import date_to_milliseconds
from binance_api import fetch_data
import plot_data

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/fetch_data_page.ui"))

class Fetch_Data_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        print('-----', self)
        self.p1_ohlcvPlot_qWebEngineView.hide()
        self.p1_saveDataToFile_button.clicked.connect(self.fetch_data_btn_clicked)

    def fetch_data_btn_clicked(self):
        start_date = self.p1_startDate_textField_day.text() + ' ' + self.p1_startDate_comboBox_month.currentText() \
                     + ' ' + self.p1_startDate_textField_year.text() + ' ' + self.p1_startDate_textField_hour.text() \
                     + ':' + self.p1_startDate_textField_minute.text() + ':' + self.p1_startDate_textField_second.text()
        end_date = self.p1_endDate_textField_day.text() + ' ' + self.p1_endDate_comboBox_month.currentText() \
                   + ' ' + self.p1_endDate_textField_year.text() + ' ' + self.p1_endDate_textField_hour.text() \
                   + ':' + self.p1_endDate_textField_minute.text() + ':' + self.p1_endDate_textField_second.text()

        currency_symbol = self.p1_cryptoSymbol_textField.text()
        interval = self.p1_interval_dropdown.currentText()
        print('currency_symbol: ', currency_symbol)
        print('interval: ', interval)
        print('start_date: ', start_date)
        print(date_to_milliseconds(start_date))
        print('end_date: ', end_date)
        print(date_to_milliseconds(end_date))
        path_to_file = QFileDialog.getSaveFileName(self, 'Save OHLCV data tpo CSV files', 'D:\!python_projects\praca_inz_qt\data', 'Text Files (*.csv)')
        fetch_data.create_csv_with_ohlcv_data(start_time=int(date_to_milliseconds(start_date)), end_time=int(date_to_milliseconds(end_date)), currency_pair_symbol=currency_symbol, interval=interval, path_to_file=path_to_file[0])
        self.p1_ohlcvPlot_qWebEngineView.show()
        self.p1_ohlcvPlot_qWebEngineView.setHtml(plot_data.plot_ohlcv_data(path_to_file[0]))


if __name__ == '__fetch_data_page__':
    import sys
    print('+++fetch_data_page')
    app = QtGui.QGuiApplication(sys.argv)
    w = Fetch_Data_Widget()
    w.show()
    sys.exit(app.exec_())
