import os
from PySide2 import QtGui, QtWidgets
from PySide2.QtUiTools import loadUiType
import utilities.plot_data as plot_data
from utilities.helpers import load_ohlcv_data_from_csv_file


current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/display_plot_page.ui"))


class Display_Plot_Page(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        self.close_button.clicked.connect(lambda: self.close_window())


    def display_candlestick_chart(self):
        self.candle_chart_widget.setHtml(plot_data.plot_ohlcv_data(load_ohlcv_data_from_csv_file()))


    def close_window(self):
        self.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = Display_Plot_Page()
    w.show()
    sys.exit(app.exec_())