import os
from PySide2 import QtGui, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtCore import Signal
import pages.strategy_page


current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/add_strategy_rule_page.ui"))


class Add_Strategy_Rule_Widget(Form, Base):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        print('-----', self)
        self.setupUi(self)
        self.p3_cancel_button.clicked.connect(lambda: self.close())
        self.p3_addRule_button.clicked.connect(self.add_rule)


    def cancel(self):
        app.quit()

    def add_rule(self):
        new_rule_to_add = self.p3_firstIndicator_comboBox.currentText() + ' ' + self.p3_firstIndicatorOptions_lineEdit.text() \
                   + ' ' + self.p3_mark_comboBox.currentText() + ' ' + self.p3_sedondIndicator_comboBox.currentText() \
                   + ' ' + self.p3_secondIndicatorOptions_lineEdit.text()
        sender = Send_Strategy_Rule()
        sender.on_send(new_rule_to_add)
        app.quit()
        return new_rule_to_add

class Send_Strategy_Rule(QtCore.QObject):
    signal = Signal()

    def on_send(self, new_rule_to_add):
        reciver = pages.strategy_page.Receive_Strategy_Rule()
        self.signal.connect(lambda: reciver.on_recive(new_rule_to_add))
        self.signal.emit()

if __name__ == '__add_strategy_rule_page__':
    import sys
    print('+++add_strategy_page')
    app = QtGui.QGuiApplication(sys.argv)
    w = Add_Strategy_Rule_Widget()
    w.show()
    sys.exit(app.exec_())
