import os
from PySide2 import QtGui, QtWidgets, QtCore
from PySide2.QtUiTools import loadUiType
from PySide2.QtWidgets import QFileDialog
from utilities.helpers import cryptocurrency_pair_dict
from utilities.plot_data import plot_ohlc_and_balance_with_transactions
import utilities.helpers
from utilities.generate_report import generate_html_report_to_file


current_dir = os.path.dirname(os.path.abspath(__file__))
Form, Base = loadUiType(os.path.join(current_dir, "../ui/summary_page.ui"))


class Summary_Page(Base, Form):
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('icons/logo2.png'))
        self.setWindowTitle('BackTesting Application')
        self.buy_rules_treeWidget.setHeaderItem(QtWidgets.QTreeWidgetItem(['Buy rules', 'Rule ID']))
        self.sell_rules_treeWidget.setHeaderItem(QtWidgets.QTreeWidgetItem(['Sell rules', 'Rule ID']))
        self.trades_dict = ''
        self.html_of_graphs = ''


    def display_buy_and_sell_rules(self, buy_rules, sell_rules, sell_simulation_settings):
        # set up buy_rules_treeWidget

        self.buy_rules_treeWidget.clear()
        buy_rules = buy_rules['buy_rules']
        QtWidgets.QTreeWidgetItem(self.buy_rules_treeWidget, [buy_rules[0]['rule_text'], buy_rules[0]['id_rule']])
        for x in range(len(buy_rules) - 1):
            for y in range(len(buy_rules)):
                if buy_rules[x + 1]['qTreeWidgetItem_Parent'] == buy_rules[y]['qTreeWidgetItem']:
                    found_parent = buy_rules[y]['rule_text']
            QtWidgets.QTreeWidgetItem(self.buy_rules_treeWidget
                                      .findItems(found_parent,
                                                 QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive,0)[-1],
                                      [buy_rules[x + 1]['rule_text'], buy_rules[x + 1]['id_rule']])
        self.buy_rules_treeWidget.expandAll()


        # set up sell_rules_treeWidget
        self.sell_rules_treeWidget.clear()
        sell_rules = sell_rules['sell_rules']
        if sell_simulation_settings['sell_settings'][0]['is_stop_loss_selected']:
            QtWidgets.QTreeWidgetItem(self.sell_rules_treeWidget,
                                      [f"Stop loss - {sell_simulation_settings['sell_settings'][0]['stop_loss']}"
                                       f" {sell_simulation_settings['sell_settings'][0]['stop_loss_unit']}",
                                       's_stop_loss'])

        if sell_simulation_settings['sell_settings'][0]['is_take_profit_selected']:
            QtWidgets.QTreeWidgetItem(self.sell_rules_treeWidget,
                                      [f"Take profit - {sell_simulation_settings['sell_settings'][0]['take_profit']}"
                                       f" {sell_simulation_settings['sell_settings'][0]['take_profit_unit']}",
                                       's_take_profit'])

        QtWidgets.QTreeWidgetItem(self.sell_rules_treeWidget, [sell_rules[0]['rule_text'], sell_rules[0]['id_rule']])
        for x in range(len(sell_rules) - 1):
            for y in range(len(sell_rules)):
                if sell_rules[x + 1]['qTreeWidgetItem_Parent'] == sell_rules[y]['qTreeWidgetItem']:
                    found_parent = sell_rules[y]['rule_text']
            QtWidgets.QTreeWidgetItem(self.sell_rules_treeWidget
                                      .findItems(found_parent,
                                                 QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive,0)[-1],
                                      [sell_rules[x + 1]['rule_text'], sell_rules[x + 1]['id_rule']])
        self.sell_rules_treeWidget.expandAll()

        self.buy_rules_treeWidget.resizeColumnToContents(0)
        self.sell_rules_treeWidget.resizeColumnToContents(0)
        if self.buy_rules_treeWidget.columnWidth(0) > self.sell_rules_treeWidget.columnWidth(0):
            self.sell_rules_treeWidget.setColumnWidth(0, self.buy_rules_treeWidget.columnWidth(0))
        else:
            self.buy_rules_treeWidget.setColumnWidth(0, self.sell_rules_treeWidget.columnWidth(0))


        self.buy_rules_treeWidget.resizeColumnToContents(1)
        self.sell_rules_treeWidget.resizeColumnToContents(1)
        if self.buy_rules_treeWidget.columnWidth(1) > self.sell_rules_treeWidget.columnWidth(1):
            self.sell_rules_treeWidget.setColumnWidth(1, self.buy_rules_treeWidget.columnWidth(1))
        else:
            self.buy_rules_treeWidget.setColumnWidth(1, self.sell_rules_treeWidget.columnWidth(1))


    def format_and_display_text(self, trades_dict, pip_position, main_window_object):
        currency_pair = (open(utilities.helpers.path_to_csv_file).readline()).rstrip("\n") # temporary solution
        currency_1_symbol = cryptocurrency_pair_dict[currency_pair]['base']
        currency_2_symbol = cryptocurrency_pair_dict[currency_pair]['quote']
        formatted_trades = ''
        balance_list = [[trades_dict['sell_trades'][0]['index'],
                         trades_dict['sell_trades'][0]['currency_2']
                         + trades_dict['sell_trades'][0]['price'] * trades_dict['sell_trades'][0]['currency_1']]]


        if trades_dict['buy_trades'][1]['index'] < trades_dict['sell_trades'][1]['index']: #first trans is buy
            for x in range(1, len(trades_dict['sell_trades'])):
                formatted_trades += '----------------------------------------------------------------------------\n'

                space_needed = (len(str(trades_dict['buy_trades'][x]['index'])) + 4 ) * ' '
                formatted_trades += '{}) > Buy: {} {}\n{}> Price: {}\n{}> Fee: {}\n{}> Rule ID: {}\n\n'\
                    .format(trades_dict['buy_trades'][x]['index'],
                            format(trades_dict['buy_trades'][x]['amount_traded'], f".{pip_position}f"),
                            currency_2_symbol,
                            space_needed,
                            trades_dict['buy_trades'][x]['price'],
                            space_needed,
                            trades_dict['buy_trades'][x]['fee'],
                            space_needed,
                            trades_dict['buy_trades'][x]['id_rule'])

                space_needed = (len(str(trades_dict['sell_trades'][x]['index'])) + 4 ) * ' '
                formatted_trades += "{}) > Sell: {} {}\n{}> Price: {}\n{}> Fee: {}\n{}> Rule ID: {}\n" \
                    .format(trades_dict['sell_trades'][x]['index'],
                            format(trades_dict['sell_trades'][x]['amount_traded'], f".{pip_position}f"),
                            currency_1_symbol,
                            space_needed,
                            trades_dict['sell_trades'][x]['price'],
                            space_needed,
                            trades_dict['sell_trades'][x]['fee'],
                            space_needed,
                            trades_dict['sell_trades'][x]['id_rule'])

                formatted_trades += '#PROFIT: {} {}\n' \
                    .format(format(trades_dict['sell_trades'][x]['currency_2']
                                   - trades_dict['sell_trades'][x-1]['currency_2']
                                   - trades_dict['sell_trades'][x-1]['currency_1']
                                   * trades_dict['sell_trades'][x-1]['price'], f".{pip_position}f"), currency_2_symbol)

                balance_list.append([trades_dict['buy_trades'][x]['index'],
                                     trades_dict['buy_trades'][x]['currency_1'] * trades_dict['buy_trades'][x]['price']
                                     ])

                balance_list.append([trades_dict['sell_trades'][x]['index'],
                                    trades_dict['sell_trades'][x]['currency_2']
                                    ])
        else: #first trans is sell
            formatted_trades += '----------------------------------------------------------------------------\n'

            space_needed = (len(str(trades_dict['sell_trades'][1]['index'])) + 4) * ' '
            formatted_trades += "{}) > Sell: {} {}\n{}> Price: {}\n{}> Fee: {}\n{}> Rule ID: {}\n"\
                .format(trades_dict['sell_trades'][1]['index'],
                        format(trades_dict['sell_trades'][1]['amount_traded'], f".{pip_position}f"),
                        currency_1_symbol,
                        space_needed,
                        trades_dict['sell_trades'][1]['price'],
                        space_needed,
                        trades_dict['sell_trades'][1]['fee'],
                        space_needed,
                        trades_dict['sell_trades'][1]['id_rule'])

            formatted_trades += '#PROFIT: {} {}\n'\
                    .format(format(trades_dict['sell_trades'][1]['currency_2']
                                   - trades_dict['sell_trades'][0]['currency_2']
                                   - trades_dict['sell_trades'][0]['currency_1']
                                   * trades_dict['sell_trades'][0]['price'], f".{pip_position}f"), currency_2_symbol)

            balance_list.append([trades_dict['sell_trades'][1]['index'],
                                trades_dict['sell_trades'][1]['currency_2']
                                ])

            for x in range(1, len(trades_dict['sell_trades'])-1):
                formatted_trades += '----------------------------------------------------------------------------\n'

                space_needed = (len(str(trades_dict['buy_trades'][x]['index'])) + 4 ) * ' '
                formatted_trades += '{}) > Buy: {} {}\n{}> Price: {}\n{}> Fee: {}\n{}> Rule ID: {}\n\n'\
                    .format(trades_dict['buy_trades'][x]['index'],
                            format(trades_dict['buy_trades'][x]['amount_traded'], f".{pip_position}f"),
                            currency_2_symbol,
                            space_needed,
                            trades_dict['buy_trades'][x]['price'],
                            space_needed,
                            trades_dict['buy_trades'][x]['fee'],
                            space_needed,
                            trades_dict['buy_trades'][x]['id_rule'])

                space_needed = (len(str(trades_dict['sell_trades'][x+1]['index'])) + 4) * ' '
                formatted_trades += '{}) > Sell: {} {}\n{}> Price: {}\n{}> Fee: {}\n{}> Rule ID: {}\n'\
                    .format(trades_dict['sell_trades'][x+1]['index'],
                            format(trades_dict['sell_trades'][x+1]['amount_traded'], f".{pip_position}f"),
                            currency_1_symbol,
                            space_needed,
                            trades_dict['sell_trades'][x+1]['price'],
                            space_needed,
                            trades_dict['sell_trades'][x+1]['fee'],
                            space_needed,
                            trades_dict['sell_trades'][x+1]['id_rule'])


                formatted_trades += '#PROFIT: {} {}\n'\
                    .format(format(trades_dict['sell_trades'][x+1]['currency_2']
                                   - trades_dict['sell_trades'][x]['currency_2']
                                   - trades_dict['sell_trades'][x]['currency_1']
                                   * trades_dict['sell_trades'][x]['price'], f".{pip_position}f"), currency_2_symbol)

                balance_list.append([trades_dict['buy_trades'][x]['index'],
                                     trades_dict['buy_trades'][x]['currency_1'] * trades_dict['buy_trades'][x]['price']
                                     ])

                balance_list.append([trades_dict['sell_trades'][x + 1]['index'],
                                    trades_dict['sell_trades'][x + 1]['currency_2']
                                    ])
        self.transactions_textBrowser.setText(formatted_trades)
        # PLOT OHLC data and balance with transactions

        html_of_graphs = plot_ohlc_and_balance_with_transactions(utilities.helpers.load_ohlcv_data_from_csv_file(),
                                                                 trades_dict,
                                                                 balance_list,
                                                                 currency_2_symbol)
        self.summary_balance_graph.setHtml(html_of_graphs)
        self.html_of_graphs = html_of_graphs
        self.trades_dict = trades_dict


    def generate_html_report(self):
        path_to_file = QFileDialog.getSaveFileName(self,
                                                   'Save simulation report',
                                                   current_dir[:-5] + "\data\\reports",
                                                   'Hyper Text Markup Language (*.html)')

        # if user click cancel on dialog window, return False and prevent program from crash
        if not path_to_file[0]:
            return False

        if self.trades_dict['buy_trades'][-1]['index'] > self.trades_dict['sell_trades'][-1]['index']:
            max_spaces = len(str(self.trades_dict['buy_trades'][-1]['index'])) + 4
        else:
            max_spaces = len(str(self.trades_dict['sell_trades'][-1]['index'])) + 4
        generate_html_report_to_file(self, self.html_of_graphs, max_spaces, path_to_file[0])


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    w = Summary_Page()
    w.show()
    sys.exit(app.exec_())