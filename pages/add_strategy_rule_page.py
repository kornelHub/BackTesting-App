import os
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtUiTools import loadUiType
from PySide2.QtCore import Signal
import pages.strategy_page

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/add_strategy_rule_page.ui"))


class Add_Strategy_Rule_Widget(Form, Base):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.p3_cancel_button.clicked.connect(lambda: self.close())
        self.add_strategy_rule_treeWidget.setHeaderLabel("")
        self.list_of_parent_text = []

    def load_QTreeWidget(self, list_of_objects):
        for element in list_of_objects:
            if element.parent() is None:
                # Add item to qTreeWidget and make is checkable
                QtWidgets.QTreeWidgetItem(self.add_strategy_rule_treeWidget, [element.text(0)]).setCheckState(0,
                                                                                                              QtCore.Qt.Unchecked)
            else:
                parent_of_current_element = self.add_strategy_rule_treeWidget.findItems(element.parent().text(0),
                                                                                        QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive,
                                                                                        0)
                # Add item to qTreeWidget and make is checkable
                QtWidgets.QTreeWidgetItem(parent_of_current_element[0], [element.text(0)]).setCheckState(0,
                                                                                                         QtCore.Qt.Unchecked)
        self.add_strategy_rule_treeWidget.expandAll()

    def add_rule(self, receive_strategy_rule_object):
        new_rule_to_add = self.p3_firstIndicator_comboBox.currentText() + ' ' + self.p3_firstIndicatorOptions_lineEdit.text() \
                          + ' ' + self.p3_mark_comboBox.currentText() + ' ' + self.p3_sedondIndicator_comboBox.currentText() \
                          + ' ' + self.p3_secondIndicatorOptions_lineEdit.text()

        #loops through  all items, if item is checked > get text of all parents
        for item in self.add_strategy_rule_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0):
            if (item.checkState(0) > 0):
                self.create_list_of_parents_text(item, [])

        print(self.list_of_parent_text)
        sender = Send_Strategy_Rule()
        sender.on_send(new_rule_to_add, self.list_of_parent_text, receive_strategy_rule_object)
        self.close()

    def create_list_of_parents_text(self, qTreeWidgetItem, helper_list):
        if qTreeWidgetItem.parent() is None:
            helper_list.append(qTreeWidgetItem.text(0))
            self.list_of_parent_text.append(helper_list)
            return True
        else:
            helper_list.append(qTreeWidgetItem.text(0))
            self.create_list_of_parents_text(qTreeWidgetItem.parent(), helper_list)


class Send_Strategy_Rule(QtCore.QObject):
    signal = Signal()

    def on_send(self, new_rule_to_add, text_of_parent_element, reciver):
        self.signal.connect(lambda: reciver.on_recive(new_rule_to_add, text_of_parent_element))
        self.signal.emit()


if __name__ == '__add_strategy_rule_page__':
    import sys

    app = QtGui.QGuiApplication(sys.argv)
    w = Add_Strategy_Rule_Widget()
    w.show()
    sys.exit(app.exec_())
