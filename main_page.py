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
        # self.showMaximized()

        self.settings_button.setIcon(QtGui.QIcon('icons/settings_icon.png'))
        self.settings_button.setIconSize(QtCore.QSize(28, 28))

        #dev helper
        self.data_path.setText("D:/!python_projects/praca_inz_qt/data/data.csv")
        utilities.helpers.path_to_csv_file = "D:/!python_projects/praca_inz_qt/data/data.csv"

        self.settings_button.clicked.connect(lambda: self.display_settings_stacked_widget())

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
        self.data_path.setText(path_to_file[0])
        utilities.helpers.path_to_csv_file = path_to_file[0]
        self.widget_pages.setCurrentIndex(0)
        self.fetch_data_page.plot_and_autofill_loaded_data()


    def display_next_stacked_widget(self):
        if self.widget_pages.currentIndex() !=2: ### disable go to settings page via next button
            if self.widget_pages.currentIndex() is 1:  ### start simulation
                from engine import simulation
                if main_widget_object.strategy_page.check_if_all_fileds_have_values():
                    simulation.init_simulation(main_widget_object)
                else:
                    return False
            self.widget_pages.setCurrentIndex(self.widget_pages.currentIndex()+1)  ### go to next page


    def display_previous_stacked_widget(self):
        if self.widget_pages.currentIndex() is 3: ### if settings_page go back to page from we came
            self.settings_page.go_back_to_previous_stacked_widget_page()
        else:
            self.widget_pages.setCurrentIndex(self.widget_pages.currentIndex()-1)  ### go to previous page


    def display_settings_stacked_widget(self):
        if not self.widget_pages.currentIndex() is 3:
            self.settings_page.store_previous_stacked_widget_index(self.widget_pages.currentIndex(), main_widget_object)
            self.widget_pages.setCurrentIndex(3)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    main_widget_object = MainWidget()
    main_widget_object.show()
    # main_widget_object.display_next_stacked_widget()
    # main_widget_object.display_next_stacked_widget()
    sys.exit(app.exec_())