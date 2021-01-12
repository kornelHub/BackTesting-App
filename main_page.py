import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtCore import Slot
from functools import partial
from pages.add_strategy_rule_page import Add_Strategy_Rule_Widget

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
        # self.showMaximized()
        self.helper_on_adding_new_rules = False

        buttons = (self.btn_menu_page_1, self.btn_menu_page_2, self.btn_menu_page_3)
        for i, button in enumerate(buttons):
            button.clicked.connect(partial(self.widget_pages.setCurrentIndex, i))

        self.btn_toggle.clicked.connect(self.toggleMenu)

########################################################################################################################
### Strategy Page ###
########################################################################################################################
        self.strategy_page.p2_add_buy_rule.clicked.connect(self.strategypage_display_add_buy_rule_page)
        self.strategy_page.p2_edit_buy_rule.clicked.connect(self.strategypage_display_modify_buy_rule_page)

        self.strategy_page.p2_add_sell_rule.clicked.connect(self.strategypage_display_sell_buy_rule_page)
        self.strategy_page.p2_edit_sell_rule.clicked.connect(self.strategypage_display_modify_sell_rule_page)


########################################################################################################################

    def strategypage_display_add_buy_rule_page(self):
        self.receive_buy_strategy_rule_to_add_object = Receive_Buy_Strategy_Rule_To_Add()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        list_of_items_in_buy_qtreewidget = self.strategy_page.p2_buyCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
        add_strategy_page_widget.load_qtreewidget(list_of_items_in_buy_qtreewidget)
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(lambda: add_strategy_page_widget.add_new_rule(self.receive_buy_strategy_rule_to_add_object))

    def strategypage_display_modify_buy_rule_page(self):
        receive_strategy_rule_to_modify_object = Receive_Strategy_Rule_To_Modify()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        add_strategy_page_widget.load_rule_details_to_modify(main_widget_object.strategy_page.p2_buyCondition_treeWidget.currentItem().text(0))
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(lambda: add_strategy_page_widget.save_modified_rule(
            main_widget_object.strategy_page.p2_buyCondition_treeWidget.currentItem(),
            receive_strategy_rule_to_modify_object))

    def strategypage_display_sell_buy_rule_page(self):
        self.receive_sell_strategy_rule_to_add_object = Receive_Sell_Strategy_Rule_To_Add()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        list_of_items_in_sell_qtreewidget = self.strategy_page.p2_sellCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
        add_strategy_page_widget.load_qtreewidget(list_of_items_in_sell_qtreewidget)
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(lambda: add_strategy_page_widget.add_new_rule(self.receive_sell_strategy_rule_to_add_object))

    def strategypage_display_modify_sell_rule_page(self):
        receive_strategy_rule_to_modify_object = Receive_Strategy_Rule_To_Modify()
        add_strategy_page_widget = Add_Strategy_Rule_Widget()
        add_strategy_page_widget.load_rule_details_to_modify(main_widget_object.strategy_page.p2_sellCondition_treeWidget.currentItem().text(0))
        add_strategy_page_widget.show()
        add_strategy_page_widget.p3_addRule_button.clicked.connect(lambda: add_strategy_page_widget.save_modified_rule(
            main_widget_object.strategy_page.p2_sellCondition_treeWidget.currentItem(),
            receive_strategy_rule_to_modify_object))

########################################################################################################################
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

    def add_parent_text_to_list(self, qTreeWidgetItem, list):
        if len(list) > 0:
            if qTreeWidgetItem.parent() is not None:
                if qTreeWidgetItem.parent().text(0) == list[0]:
                    self.add_parent_text_to_list(qTreeWidgetItem.parent(), list[1:])
                else:
                    main_widget_object.helper_on_adding_new_rules = False
                    return False
            else:
                main_widget_object.helper_on_adding_new_rules = True
                return True
        else:
            main_widget_object.helper_on_adding_new_rules = True
            return True

### Add new rule receivers
class Receive_Buy_Strategy_Rule_To_Add(QtCore.QObject):
    @Slot(str)
    def receive_and_add_rule(self, received_rule, text_of_parent_element):
        if len(text_of_parent_element) > 0:
            for list_in_list in text_of_parent_element:
                if len(list_in_list) > 0:
                    for found_element in main_widget_object.strategy_page.p2_buyCondition_treeWidget.findItems(
                            list_in_list[0], QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0):
                        main_widget_object.add_parent_text_to_list(found_element, list_in_list[1:])
                        if main_widget_object.helper_on_adding_new_rules:
                            QtWidgets.QTreeWidgetItem(found_element, [received_rule])
        else:
            QtWidgets.QTreeWidgetItem(main_widget_object.strategy_page.p2_buyCondition_treeWidget, [received_rule])
        main_widget_object.strategy_page.p2_buyCondition_treeWidget.expandAll()

class Receive_Sell_Strategy_Rule_To_Add(QtCore.QObject):
    @Slot(str)
    def receive_and_add_rule(self, received_rule, text_of_parent_element):
        if len(text_of_parent_element) > 0:
            for list_in_list in text_of_parent_element:
                if len(list_in_list) > 0:
                    for found_element in main_widget_object.strategy_page.p2_sellCondition_treeWidget.findItems(
                            list_in_list[0], QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0):
                        main_widget_object.add_parent_text_to_list(found_element, list_in_list[1:])
                        if main_widget_object.helper_on_adding_new_rules:
                            QtWidgets.QTreeWidgetItem(found_element, [received_rule])
        else:
            QtWidgets.QTreeWidgetItem(main_widget_object.strategy_page.p2_sellCondition_treeWidget, [received_rule])
        main_widget_object.strategy_page.p2_sellCondition_treeWidget.expandAll()

### Modify rule receiver
class Receive_Strategy_Rule_To_Modify(QtCore.QObject):
    @Slot(str)
    def receive_and_modify_rule(self, received_rule, current_selected_item):
        current_selected_item.setText(0, received_rule)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    main_widget_object = MainWidget()
    main_widget_object.show()
    sys.exit(app.exec_())