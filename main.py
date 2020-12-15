# import sys
# import platform
# from PySide2 import QtCore, QtGui, QtWidgets
# from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
# from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
# from PySide2.QtWidgets import *
# from PySide2.QtUiTools import QUiLoader
#
#
# from ui_functions import *
# from binance_api import fetch_data
# import plot_data
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         QMainWindow.__init__(self)
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
#         self.setWindowTitle('BackTesting Application')
#         self.ui.p1_ohlcvPlot_qWebEngineView.hide()
#
#         ## TOGGLE/BURGUER MENU
#         ########################################################################
#         self.ui.btn_toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))
#
#         ## PAGES
#         ########################################################################
#
#         # PAGE 1
#         self.ui.btn_menu_page_1.clicked.connect(lambda: self.ui.widget_pages.setCurrentWidget(self.ui.page_1))
#         # GET OHLVC DATA
#         self.ui.p1_saveDataToFile_button.clicked.connect(lambda: UIFunctions.fetch_data_btn_clicked(self))
#
#         ########################################################################
#
#         # PAGE 2
#         self.ui.btn_menu_page_2.clicked.connect(lambda: self.ui.widget_pages.setCurrentWidget(self.ui.page_2))
#         self.ui.p2_addBuyCondition_button.clicked.connect(lambda: UIFunctions.add_buy_condition(self))
#         self.ui.p2_addSellCondition_button.clicked.connect(lambda: UIFunctions.add_sell_condition(self))
#
#         # PAGE 3
#         self.ui.btn_menu_page_3.clicked.connect(lambda: self.ui.widget_pages.setCurrentWidget(self.ui.page_3))
#
#         ## SHOW ==> MAIN WINDOW
#         ########################################################################
#         self.show()
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     sys.exit(app.exec_())

import os
from PySide2 import QtGui, QtWidgets, QtWebEngineWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from functools import partial
from pages.ui_functions import *

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

        buttons = (self.btn_menu_page_1, self.btn_menu_page_2, self.btn_menu_page_3)
        for i, button in enumerate(buttons):
            button.clicked.connect(partial(self.widget_pages.setCurrentIndex, i))

        self.btn_toggle.clicked.connect(self.toggleMenu)

    def toggleMenu(self):
        # GET WIDTH
        width = self.frame_left_menu_container.width()
        maxExtend = 250
        standard = 70

        # SET MAX WIDTH
        if width == 70:
            widthExtended = maxExtend
        else:
            widthExtended = standard

        # ANIMATION
        self.animation = QtCore.QPropertyAnimation(self.frame_left_menu_container, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setStartValue(width)
        self.animation.setEndValue(widthExtended)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())