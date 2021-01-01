import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from functools import partial

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "ui/mainWindow.ui"))

class MainWidget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        print('-----', self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        self.btn_toggle.setIcon(QtGui.QPixmap('icons/menu.png'))
        self.btn_toggle.setIconSize(QtCore.QSize(32, 32))
        # self.showMaximized()

        buttons = (self.btn_menu_page_1, self.btn_menu_page_2, self.btn_menu_page_3)
        for i, button in enumerate(buttons):
            button.clicked.connect(partial(self.widget_pages.setCurrentIndex, i))

        self.btn_toggle.clicked.connect(self.toggleMenu)
        # print(self.widget_pages.currentWidget().fetch_data_btn_clicked())

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


def mainFunc():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    print('+++main')
    app.setStyle("fusion")
    window = MainWidget()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    mainFunc()