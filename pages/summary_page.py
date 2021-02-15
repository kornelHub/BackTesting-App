import os
from PySide2 import QtGui, QtWidgets
from PySide2.QtUiTools import loadUiType
from pages.display_plot_page import Display_Plot_Page


current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/summary_page.ui"))


class Summary_Page(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        currency_pair = open('data/data.csv').readline()
        print(currency_pair)


    def plot_candle_chart(self):
        display_plot_page = Display_Plot_Page()
        display_plot_page.display_candlestick_chart()
        display_plot_page.show()


    def format_and_dislay_text(self, trades_dict):
        formatted_trades = ''
        if trades_dict['buy_trades'][1]['index'] < trades_dict['sell_trades'][1]['index']: #first trans is buy
            for x in range(len(trades_dict['sell_trades'])-1):
                formatted_trades += '----------------------------------------------------------------------------\n'
                formatted_trades += '{}) BOUGHT {} for price {}\n' \
                    .format(trades_dict['buy_trades'][x+1]['index'],
                            trades_dict['buy_trades'][x+1]['amount_traded'],
                            trades_dict['buy_trades'][x+1]['price'])
                formatted_trades += '{}) SOLD {} for price {}\n' \
                    .format(trades_dict['sell_trades'][x+1]['index'],
                            trades_dict['sell_trades'][x+1]['amount_traded'],
                            trades_dict['sell_trades'][x+1]['price'])
                formatted_trades += '#PROFIT: {}\n' \
                    .format(trades_dict['sell_trades'][x+1]['currency_2'] - trades_dict['sell_trades'][x]['currency_2']
                                - trades_dict['sell_trades'][x]['currency_1'] * trades_dict['sell_trades'][x]['price'])
        else: #first trans is sell
            formatted_trades += '----------------------------------------------------------------------------\n'
            formatted_trades += '{}) SOLD {} for price {}\n'\
                .format(trades_dict['sell_trades'][1]['index'],
                        trades_dict['sell_trades'][1]['amount_traded'],
                        trades_dict['sell_trades'][1]['price'])
            formatted_trades += '#PROFIT: {}\n'\
                    .format(trades_dict['sell_trades'][1]['currency_2'] - trades_dict['sell_trades'][0]['currency_2']
                                - trades_dict['sell_trades'][0]['currency_1'] * trades_dict['sell_trades'][0]['price'])
            for x in range(len(trades_dict['sell_trades'])-2):
                formatted_trades += '----------------------------------------------------------------------------\n'
                formatted_trades += '{}) BOUGHT {} for price {}\n'\
                    .format(trades_dict['buy_trades'][x+1]['index'],
                            trades_dict['buy_trades'][x+1]['amount_traded'],
                            trades_dict['buy_trades'][x+1]['price'])
                formatted_trades += '{}) SOLD {} for price {}\n'\
                    .format(trades_dict['sell_trades'][x+2]['index'],
                            trades_dict['sell_trades'][x+2]['amount_traded'],
                            trades_dict['sell_trades'][x+2]['price'])
                formatted_trades += '#PROFIT: {}\n'\
                    .format(trades_dict['sell_trades'][x+2]['currency_2'] - trades_dict['sell_trades'][x+1]['currency_2']
                                - trades_dict['sell_trades'][x+1]['currency_1'] * trades_dict['sell_trades'][x+1]['price'])
        self.textBrowser.setText(formatted_trades)


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = Summary_Page()
    w.show()
    sys.exit(app.exec_())