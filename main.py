import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

from mainWindow import Ui_MainWindow
from ui_functions import *
from binance_api import fetch_data
import plot_data

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        self.ui.p1_ohlcvPlot_qWebEngineView.hide()

        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.ui.btn_toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))

        ## PAGES
        ########################################################################

        # PAGE 1
        self.ui.btn_menu_page_1.clicked.connect(lambda: self.ui.widget_pages.setCurrentWidget(self.ui.page_1))
        # GET OHLVC DATA
        self.ui.p1_saveDataToFile_button.clicked.connect(lambda: UIFunctions.fetch_data_btn_clicked(self))

        ########################################################################

        # PAGE 2
        self.ui.btn_menu_page_2.clicked.connect(lambda: self.ui.widget_pages.setCurrentWidget(self.ui.page_2))
        self.ui.p2_addBuyCondition_button.clicked.connect(lambda: UIFunctions.add_buy_condition(self))
        self.ui.p2_addSellCondition_button.clicked.connect(lambda: UIFunctions.add_sell_condition(self))

        # PAGE 3
        self.ui.btn_menu_page_3.clicked.connect(lambda: self.ui.widget_pages.setCurrentWidget(self.ui.page_3))
        # self.ui.pushButton.connect()


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

