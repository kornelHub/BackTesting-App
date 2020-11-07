from main import *

class UIFunctions(MainWindow):
    def toggleMenu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.ui.frame_left_menu_container.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.frame_left_menu_container, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def fetch_data_btn_clicked(self):
        end_date = self.ui.p1_endDate_textField.text()
        start_date = self.ui.p1_startDate_textField.text()
        currency_symbol = self.ui.p1_cryptoSymbol_textField.text()
        interval = self.ui.p1_interval_dropdown.currentText()
        print('start_date: ', start_date)
        print('end_date: ', end_date)
        print('currency_symbol: ', currency_symbol)
        print('interval: ', interval)
        path_to_file = QFileDialog.getSaveFileName(self, 'Save OHLCV data tpo CSV files', 'D:\!python_projects\praca_inz_qt\data', 'Text Files (*.csv)')
        fetch_data.create_csv_with_ohlcv_data(start_time=int(start_date), end_time=int(end_date), currency_pair_symbol=currency_symbol, interval=interval, path_to_file=path_to_file[0])
        self.ui.p1_ohlcvPlot_qWebEngineView.show()
        self.ui.p1_ohlcvPlot_qWebEngineView.setHtml(plot_data.plot_ohlcv_data(path_to_file[0]))

    ########################################################################

    def add_buy_condition(self):
        buy_level_1 = QtWidgets.QTreeWidgetItem(self.ui.p2_buyCondition_treeWidget, ["lorem ipsu"])
        buy_level_2 = QtWidgets.QTreeWidgetItem(buy_level_1, ["lorem ipsu2"])

    def add_sell_condition(self):
        sell_level_1 = QtWidgets.QTreeWidgetItem(self.ui.p2_sellCondition_treeWidget, ["lorem ipsu"])
        sell_level_2 = QtWidgets.QTreeWidgetItem(sell_level_1, ["lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2lorem ipsu2"])
        sell_level_3 = QtWidgets.QTreeWidgetItem(sell_level_2, ["lorem ipsu3"])
        sell_level_4 = QtWidgets.QTreeWidgetItem(sell_level_3, ["lorem ipsu4"])

        sell_level_1.setBackground(0, QtGui.QColor(170, 14, 9))
        sell_level_2.setBackground(0, QtGui.QColor(220, 9, 9))
        sell_level_3.setBackground(0, QtGui.QColor(246, 35, 35))
        sell_level_4.setBackground(0, QtGui.QColor(248, 84, 84))