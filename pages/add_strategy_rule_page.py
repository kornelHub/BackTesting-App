import os
from PySide2 import QtGui
from PySide2.QtUiTools import loadUiType

current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/add_strategy_rule_page.ui"))


class Add_Strategy_Rule_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.p3_cancel_button.clicked.connect(self.cancel)
        self.p3_addRule_button.clicked.connect(self.add_rule)


    def cancel(self):
        print('CANCEL')

    def add_rule(self):
        print('RULE ADDED')

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    w = Add_Strategy_Rule_Widget()
    w.show()
    sys.exit(app.exec_())
