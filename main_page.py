import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QFileDialog
from functools import partial
import utilities.helpers

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "ui/mainWindow.ui"))

class MainWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        self.btn_toggle.setIcon(QtGui.QPixmap('icons/menu.png'))
        self.btn_toggle.setIconSize(QtCore.QSize(32, 32))
        self.data_path.setReadOnly(True)
        # self.showMaximized()

        #dev helper
        self.data_path.setText("D:/!python_projects/praca_inz_qt/data/data.csv")
        utilities.helpers.path_to_csv_file = "D:/!python_projects/praca_inz_qt/data/data.csv"

        buttons = (self.btn_menu_page_1, self.btn_menu_page_2, self.btn_menu_page_3)
        for i, button in enumerate(buttons):
            button.clicked.connect(partial(self.widget_pages.setCurrentIndex, i))

        # Top toolbar menu
        self.btn_toggle.clicked.connect(lambda: self.toggleMenu())
        self.load_data_button.clicked.connect(lambda: self.load_data_from_file())
        self.next_btn.clicked.connect(lambda: self.display_next_page())

        # Strategy page
        self.strategy_page.p2_add_buy_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_buy_context(main_widget_object.strategy_page))
        self.strategy_page.p2_edit_buy_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_modify_buy_context())

        self.strategy_page.p2_add_sell_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_sell_context(main_widget_object.strategy_page))
        self.strategy_page.p2_edit_sell_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_modify_sell_context())

        # Fetch data page
        self.fetch_data_page.p1_saveDataToFile_button.clicked.connect(lambda: self.fetch_data_page.fetch_data_btn_clicked(main_widget_object, current_dir))

    def toggleMenu(self):
        width = self.frame_left_menu_container.width()
        maxExtend = 250
        standard = 70
        if width == 70:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        self.animation = QtCore.QPropertyAnimation(self.frame_left_menu_container, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def load_data_from_file(self):
        path_to_file = QFileDialog.getOpenFileName(self, 'Load CSV file with OHLCV data', current_dir + '\data', 'Text Files (*.csv)')
        self.data_path.setText(path_to_file[0])
        utilities.helpers.path_to_csv_file = path_to_file[0]
        self.widget_pages.setCurrentIndex(0)
        self.fetch_data_page.plot_and_autofill_loaded_data()


    def display_next_page(self):
        ### start simulation
        if self.widget_pages.currentIndex() is 1:
            from engine import simulation
            simulation.init_simulation(main_widget_object)
        self.widget_pages.setCurrentIndex(self.widget_pages.currentIndex()+1)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    main_widget_object = MainWidget()
    main_widget_object.show()
    sys.exit(app.exec_())