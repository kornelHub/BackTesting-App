import os
from PySide2 import QtGui, QtWidgets
from PySide2.QtUiTools import loadUiType
from pages.display_plot_page import Display_Plot_Page
from utilities.helpers import cryptocurrency_pair_dict
from utilities.plot_data import plot_balance


current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/summary_page.ui"))


class Summary_Page(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')



    def plot_candle_chart(self):
        display_plot_page = Display_Plot_Page()
        display_plot_page.display_candlestick_chart()
        display_plot_page.show()


    def format_and_display_text(self, trades_dict):
        currency_pair = (open('data/data.csv').readline()).rstrip("\n") # temporary solution
        currency_1 = cryptocurrency_pair_dict[currency_pair]['base']
        currency_2 = cryptocurrency_pair_dict[currency_pair]['quote']
        formatted_trades = ''
        balance_list = []


        if trades_dict['buy_trades'][1]['index'] < trades_dict['sell_trades'][1]['index']: #first trans is buy
            for x in range(1, len(trades_dict['sell_trades'])):
                formatted_trades += '----------------------------------------------------------------------------\n'

                formatted_trades += '{}) Bought {} {} for price {}\n' \
                    .format(trades_dict['buy_trades'][x]['index'],
                            trades_dict['buy_trades'][x]['amount_traded'],
                            currency_2,
                            trades_dict['buy_trades'][x]['price'])

                formatted_trades += '{}) Sold {} {} for price {}\n' \
                    .format(trades_dict['sell_trades'][x]['index'],
                            trades_dict['sell_trades'][x]['amount_traded'],
                            currency_1,
                            trades_dict['sell_trades'][x]['price'])

                formatted_trades += '#PROFIT: {}\n' \
                    .format(trades_dict['sell_trades'][x]['currency_2'] - trades_dict['sell_trades'][x-1]['currency_2']
                                - trades_dict['sell_trades'][x-1]['currency_1'] * trades_dict['sell_trades'][x-1]['price'])

                balance_list.append([trades_dict['sell_trades'][x]['index'],
                                    trades_dict['sell_trades'][x]['currency_2']
                                    # - trades_dict['sell_trades'][x - 1]['currency_2']
                                    # - trades_dict['sell_trades'][x - 1]['currency_1'] *trades_dict['sell_trades'][x - 1]['price']
                                    ])
        else: #first trans is sell
            formatted_trades += '----------------------------------------------------------------------------\n'

            formatted_trades += '{}) Sold {} {} for price {}\n'\
                .format(trades_dict['sell_trades'][1]['index'],
                        trades_dict['sell_trades'][1]['amount_traded'],
                        currency_1,
                        trades_dict['sell_trades'][1]['price'])

            formatted_trades += '#PROFIT: {}\n'\
                    .format(trades_dict['sell_trades'][1]['currency_2'] - trades_dict['sell_trades'][0]['currency_2']
                                - trades_dict['sell_trades'][0]['currency_1'] * trades_dict['sell_trades'][0]['price'])

            balance_list.append([trades_dict['sell_trades'][1]['index'],
                                trades_dict['sell_trades'][1]['currency_2']
                                # - trades_dict['sell_trades'][0]['currency_2']
                                # - trades_dict['sell_trades'][0]['currency_1'] * trades_dict['sell_trades'][0]['price']
                                ])

            for x in range(1, len(trades_dict['sell_trades'])-1):
                formatted_trades += '----------------------------------------------------------------------------\n'

                formatted_trades += '{}) Bought {} {} for price {}\n'\
                    .format(trades_dict['buy_trades'][x]['index'],
                            trades_dict['buy_trades'][x]['amount_traded'],
                            currency_2,
                            trades_dict['buy_trades'][x]['price'])

                formatted_trades += '{}) Sold {} {} for price {}\n'\
                    .format(trades_dict['sell_trades'][x+1]['index'],
                            trades_dict['sell_trades'][x+1]['amount_traded'],
                            currency_1,
                            trades_dict['sell_trades'][x+1]['price'])


                formatted_trades += '#PROFIT: {}\n'\
                    .format(trades_dict['sell_trades'][x+1]['currency_2'] - trades_dict['sell_trades'][x]['currency_2']
                                - trades_dict['sell_trades'][x]['currency_1'] * trades_dict['sell_trades'][x]['price'])

                balance_list.append([trades_dict['sell_trades'][x+1]['index'],
                                    trades_dict['sell_trades'][x + 1]['currency_2']
                                    # - trades_dict['sell_trades'][x]['currency_2']
                                    # - trades_dict['sell_trades'][x]['currency_1'] * trades_dict['sell_trades'][x]['price']
                                    ])
        self.textBrowser.setText(formatted_trades)
        self.summary_balance_graph.setHtml(plot_balance(balance_list))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = Summary_Page()
    w.show()
    sys.exit(app.exec_())