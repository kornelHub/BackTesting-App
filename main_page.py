import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from functools import partial
from engine import simulation

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
        self.strategy_path.setReadOnly(True)
        # self.showMaximized()

        buttons = (self.btn_menu_page_1, self.btn_menu_page_2, self.btn_menu_page_3)
        for i, button in enumerate(buttons):
            button.clicked.connect(partial(self.widget_pages.setCurrentIndex, i))

        self.btn_toggle.clicked.connect(self.toggleMenu)
        self.next_btn.clicked.connect(lambda: self.display_next_page())

########################################################################################################################
### Strategy Page ###
########################################################################################################################
        self.strategy_page.p2_add_buy_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_buy_context(main_widget_object.strategy_page))
        self.strategy_page.p2_edit_buy_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_modify_buy_context())

        self.strategy_page.p2_add_sell_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_sell_context(main_widget_object.strategy_page))
        self.strategy_page.p2_edit_sell_rule.clicked.connect(lambda: self.strategy_page.display_add_strategy_rule_page_modify_sell_context())
########################################################################################################################
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

    def display_next_page(self):
        ### start simulation
        if self.widget_pages.currentIndex() is 1:
            simulation.init_simulation(main_widget_object)
        self.widget_pages.setCurrentIndex(self.widget_pages.currentIndex()+1)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    main_widget_object = MainWidget()
    main_widget_object.show()
    sys.exit(app.exec_())