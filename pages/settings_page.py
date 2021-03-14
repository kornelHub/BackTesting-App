import os
from PySide2 import QtGui, QtWidgets
from PySide2.QtUiTools import loadUiType
import configparser


current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/settings_page.ui"))


class Settings_Widget(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        self.close_button.clicked.connect(lambda: self.close_window())
        self.save_settings_button.clicked.connect(lambda: self.save_settings())

        #load configuration values from file is exist
        if os.path.exists(current_dir[:-5]+'config.ini'):
            config = configparser.ConfigParser()
            config.read(current_dir[:-5]+'config.ini')
            self.public_key_plainTextEdit.setPlainText(config['user_binance_api_key']['public_key'])
            self.secret_key_plainTextEdit.setPlainText(config['user_binance_api_key']['secret_key'])


    def save_settings(self):
        if not os.path.exists(current_dir[:-5]+'config.ini'):
            cfgfile = open(current_dir[:-5]+'config.ini', 'w')
            config = configparser.ConfigParser()
            config.add_section('user_binance_api_key')
            config.set('user_binance_api_key', 'public_key', self.public_key_plainTextEdit.toPlainText())
            config.set('user_binance_api_key', 'secret_key', self.secret_key_plainTextEdit.toPlainText())
            config.write(cfgfile)
            cfgfile.close()

    def close_window(self):
        self.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = Settings_Widget()
    w.show()
    sys.exit(app.exec_())