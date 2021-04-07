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
        self.close_button.clicked.connect(lambda: self.go_back_to_previous_stacked_widget_page())
        self.save_settings_button.clicked.connect(lambda: self.save_settings())
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setText("<a href='https://www.binance.com/en-NG/support/faq/360002502072'>Tutorial</a>")

        #load configuration values from file is exist
        if os.path.exists(current_dir[:-5]+'config.ini'):
            config = configparser.ConfigParser()
            config.read(current_dir[:-5]+'config.ini')
            self.public_key_plainTextEdit.setPlainText(config['user_binance_api_key']['public_key'])
            self.secret_key_plainTextEdit.setPlainText(config['user_binance_api_key']['secret_key'])


    def save_settings(self):
        # if not os.path.exists(current_dir[:-5]+'config.ini'):
        cfgfile = open(current_dir[:-5]+'config.ini', 'w')
        config = configparser.ConfigParser()
        config.add_section('user_binance_api_key')
        config.set('user_binance_api_key', 'public_key', self.public_key_plainTextEdit.toPlainText())
        config.set('user_binance_api_key', 'secret_key', self.secret_key_plainTextEdit.toPlainText())
        config.write(cfgfile)
        cfgfile.close()
        self.go_back_to_previous_stacked_widget_page()

    def go_back_to_previous_stacked_widget_page(self):
        main_window.widget_pages.setCurrentIndex(previous_stacked_widget_index_value)

    def store_previous_stacked_widget_index(self, previous_stacked_widget_index, main_window_object):
        global previous_stacked_widget_index_value
        previous_stacked_widget_index_value = previous_stacked_widget_index
        global main_window
        main_window = main_window_object

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = Settings_Widget()
    w.show()
    sys.exit(app.exec_())