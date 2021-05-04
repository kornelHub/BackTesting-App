import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QFileDialog
import utilities.helpers

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "ui/mainWindow.ui"))

class MainWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        self.data_path.setReadOnly(True)
        self.showMaximized()
        # self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False)

        self.settings_button.setIcon(QtGui.QIcon('icons/settings_icon.png'))
        self.settings_button.setIconSize(QtCore.QSize(28, 28))

        self.save_button.setIcon(QtGui.QIcon('icons/save_icon.png'))
        self.save_button.setIconSize(QtCore.QSize(28, 28))
        self.save_button.hide()
        self.line_3.hide()


        self.settings_button.clicked.connect(lambda: self.display_settings_page())

        # Top toolbar menu
        self.load_data_button.clicked.connect(lambda: self.load_data_from_file())
        self.next_page_btn.clicked.connect(lambda: self.display_next_stacked_widget())
        self.previous_page_btn.clicked.connect(lambda: self.display_previous_stacked_widget())

        # Strategy page
        self.strategy_page.p2_add_buy_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_buy_context(main_widget_object.strategy_page))
        self.strategy_page.p2_edit_buy_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_modify_buy_context())

        self.strategy_page.p2_add_sell_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_sell_context(main_widget_object.strategy_page))
        self.strategy_page.p2_edit_sell_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_modify_sell_context())

        # Fetch data page
        self.fetch_data_page.p1_saveDataToFile_button.clicked.connect(lambda: self.fetch_data_page.fetch_data_btn_clicked(main_widget_object, current_dir))


    def load_data_from_file(self):
        path_to_file = QFileDialog.getOpenFileName(self, 'Load CSV file with OHLCV data', current_dir + '\data', 'Text Files (*.csv)')
        if path_to_file[0]:
            self.display_fetch_data_page()
            if '.csv' in path_to_file[0]:
                if utilities.helpers.columns_name_string in open(path_to_file[0]).readlines()[1]:
                    self.data_path.setText(path_to_file[0])
                    utilities.helpers.path_to_csv_file = path_to_file[0]
                    self.fetch_data_page.plot_and_autofill_loaded_data()
                    self.data_path.setProperty('invalid', False)
                    self.data_path.style().polish(self.data_path)
                else:
                    utilities.helpers.show_error_message(self.fetch_data_page.error_message_label,
                                                         'Pleas load valid CSV file with OHLC data to continue.')
                    self.data_path.setProperty('invalid', True)
                    self.data_path.style().polish(self.data_path)
            else:
                utilities.helpers.show_error_message(self.fetch_data_page.error_message_label,
                                                     'Pleas load CSV file with OHLC data to continue.')
                self.data_path.setProperty('invalid', True)
                self.data_path.style().polish(self.data_path)


    def display_next_stacked_widget(self):
        if self.widget_pages.currentIndex() is 0:
            self.display_strategy_page()
        elif self.widget_pages.currentIndex() is 1:
            self.display_summary_page()


    def display_previous_stacked_widget(self):
        if self.widget_pages.currentIndex() is 1:
            self.display_fetch_data_page()
        elif self.widget_pages.currentIndex() is 2:
            self.display_strategy_page()
        elif self.widget_pages.currentIndex() is 3:
            self.settings_page.go_back_to_previous_stacked_widget_page()


    def display_fetch_data_page(self):
        self.set_forbidden_cursor(self.previous_page_btn)
        self.set_default_cursor(self.next_page_btn)
        self.hide_save_icon()
        self.widget_pages.setCurrentIndex(0)


    def display_strategy_page(self):
        if main_widget_object.fetch_data_page.check_if_ohlc_file_is_selected(main_widget_object):
            self.set_default_cursor(self.previous_page_btn)
            self.set_default_cursor(self.next_page_btn)
            self.hide_save_icon()
            self.widget_pages.setCurrentIndex(1)


    def display_summary_page(self):
        if main_widget_object.strategy_page.check_if_all_fileds_have_values():
            from engine import simulation
            simulation.init_simulation(main_widget_object)
            self.show_save_icon()
            self.set_default_cursor(self.previous_page_btn)
            self.set_forbidden_cursor(self.next_page_btn)
            self.widget_pages.setCurrentIndex(2)
        else:
            return False


    def display_settings_page(self):
        if not self.widget_pages.currentIndex() is 3:
            self.settings_page.store_previous_stacked_widget_index(self.widget_pages.currentIndex(), main_widget_object)
            self.hide_save_icon()
            self.set_default_cursor(self.previous_page_btn)
            self.set_forbidden_cursor(self.next_page_btn)
            self.widget_pages.setCurrentIndex(3)


    def set_forbidden_cursor(self, element):
        element.setCursor(QtCore.Qt.ForbiddenCursor)
        

    def set_default_cursor(self, element):
        element.setCursor(QtCore.Qt.ArrowCursor)


    def hide_save_icon(self):
        self.save_button.hide()
        self.line_3.hide()


    def show_save_icon(self):
        self.save_button.show()
        self.line_3.show()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    main_widget_object = MainWidget()
    main_widget_object.show()
    sys.exit(app.exec_())