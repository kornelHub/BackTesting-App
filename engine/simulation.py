from PySide2 import QtCore
import helpers.helpers as helpers
import pandas as pd
import json


def get_buy_rules(strategy_page):
    list_of_items_in_buy_and_text = {'buy_rules': []}
    list_of_items_in_buy_qtreewidget = strategy_page.p2_buyCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
    for buy_item in list_of_items_in_buy_qtreewidget:
        list_of_items_in_buy_and_text['buy_rules'].append({
            'qTreeWidgetItem': buy_item,
            'rule_text': buy_item.text(0),
            'qTreeWidgetItem_Parent': buy_item.parent(),
            'if_statement': ''})
    return list_of_items_in_buy_and_text


def get_sell_rules(strategy_page):
    list_of_items_in_sell_and_text = {'sell_rules': []}
    list_of_items_in_sell_qtreewidget = strategy_page.p2_sellCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
    for sell_item in list_of_items_in_sell_qtreewidget:
        list_of_items_in_sell_and_text['sell_rules'].append({
            'qTreeWidgetItem': sell_item,
            'rule_text': sell_item.text(0),
            'qTreeWidgetItem_Parent': sell_item.parent(),
            'if_statement': ''})
    return list_of_items_in_sell_and_text


def slice_rule(rule):
    first_indicator_short_name = rule[:rule.find('(') - 1]
    rule = rule[rule.find('('):]
    first_indicator_options = rule[:rule.find('[') - 1]
    rule = rule[rule.find('['):]
    first_indicator_period = rule[:rule.find(']') + 1]
    rule = rule[rule.find(']') + 2:]
    math_char = rule[:2].strip()
    rule = rule[2:].strip()
    second_indicator_short_name = rule[:rule.find('(') - 1]
    rule = rule[rule.find('('):]
    second_indicator_options = rule[:rule.find('[') - 1]
    rule = rule[rule.find('['):]
    second_indicator_period = rule

    if first_indicator_options != '(-)':   # menage indicators with no parameters
        first_indicator_options = first_indicator_options[1:-1]
        first_indicator_options_list = []
        buy_coma_count = first_indicator_options.count(',')
        if buy_coma_count == 0:
            first_indicator_options_list.append(first_indicator_options)
        else:
            for coma in range(buy_coma_count):
                first_indicator_options_list.append(first_indicator_options[:first_indicator_options.find(',')])
                first_indicator_options = first_indicator_options[first_indicator_options.find(',') + 2:]
                if coma == buy_coma_count - 1:
                    first_indicator_options_list.append(first_indicator_options)
    else:
        first_indicator_options_list = []

    if second_indicator_options != '(-)':   # menage indicators with no parameters
        second_indicator_options = second_indicator_options[1:-1]
        second_indicator_options_list = []
        sell_coma_count = second_indicator_options.count(',')
        if sell_coma_count == 0:
            second_indicator_options_list.append(second_indicator_options)
        else:
            for coma in range(sell_coma_count):
                second_indicator_options_list.append(second_indicator_options[:second_indicator_options.find(',')])
                second_indicator_options = second_indicator_options[second_indicator_options.find(',') + 2:]
                if coma == sell_coma_count - 1:
                    second_indicator_options_list.append(second_indicator_options)
    else:
        second_indicator_options_list = []

    return first_indicator_short_name, first_indicator_options_list, first_indicator_period, math_char, \
           second_indicator_short_name, second_indicator_options_list, second_indicator_period


def build_column_name(indicator_short_name, indicator_options_list):
    combined_column_name = ''
    if indicator_short_name == 'Value':
        # this is used on purpose, Open is always in data_df
        return 'Open'
    elif indicator_short_name == 'Open' or indicator_short_name == 'High' or indicator_short_name == 'Low' \
            or indicator_short_name == 'Close' or indicator_short_name == 'Volume':
        combined_column_name = indicator_short_name
    elif indicator_short_name == 'BOLL - Upper Band':
        combined_column_name = 'BOLL_Upper'
    elif indicator_short_name == 'BOLL - Lower Band':
        combined_column_name = 'BOLL_Lower'
    elif indicator_short_name == 'MACD - MACD Line':
        combined_column_name = 'MACD_Line'
    elif indicator_short_name == 'MACD - Singal Line':
        combined_column_name = 'MACD_Signal_Line'
    else:
        combined_column_name = indicator_short_name

    for element in indicator_options_list:
        combined_column_name += '_' + element

    return combined_column_name


def build_if_statement(first_indicator_short_name, first_indicator_options_list, first_indicator_period,
                       math_char,
                       second_indicator_short_name, second_indicator_options_list, second_indicator_period):
    if first_indicator_short_name == 'Value':
        if_statement_first_part = first_indicator_options_list[0] + ' '
    else:
        first_indicator_collumn_name = build_column_name(first_indicator_short_name, first_indicator_options_list)
        first_indicator_period = first_indicator_period[1:-1]  # remove square bracket
        if_statement_first_part = f"if data_df.iloc[x+{first_indicator_period}]['{first_indicator_collumn_name}'] "

    if second_indicator_short_name == 'Value':
        if_statement_second_part = ' ' + second_indicator_options_list[0] + ':'
    else:
        second_indicator_collumn_name = build_column_name(second_indicator_short_name, second_indicator_options_list)
        second_indicator_period = second_indicator_period[1:-1]  # remove square bracket
        if_statement_second_part = f" data_df.iloc[x+{second_indicator_period}]['{second_indicator_collumn_name}']:"

    if_statement = if_statement_first_part + math_char + if_statement_second_part
    return if_statement


def glue_if_statements(list_of_rules, context):
    if_statement = ""
    for x in range(len(list_of_rules)):
        if_statement += "\t" * (check_if_parent_exist(list_of_rules[x]['qTreeWidgetItem'], 0) + 1) + list_of_rules[x]['if_statement'] + "\n"
        if len(list_of_rules) > x + 1:
            if check_if_parent_exist(list_of_rules[x]['qTreeWidgetItem'], 0) >= check_if_parent_exist(list_of_rules[x + 1]['qTreeWidgetItem'], 0):
                if_statement += "\t" * (check_if_parent_exist(list_of_rules[x]['qTreeWidgetItem'], 0) + 2) + f"{context}(x, {context}_simulation_settings, trades_dict)\n"
                if_statement += "\t" * (check_if_parent_exist(list_of_rules[x]['qTreeWidgetItem'], 0) + 2) + "continue\n"
        else:
            if_statement += "\t" * (check_if_parent_exist(list_of_rules[x]['qTreeWidgetItem'], 0) + 2) + f"{context}(x, {context}_simulation_settings, trades_dict)\n"
            if_statement += "\t" * (check_if_parent_exist(list_of_rules[x]['qTreeWidgetItem'], 0) + 2) + "continue\n"

    return if_statement


# helper function to glue_if_statements()
def check_if_parent_exist(item, parent_number):
    if item.parent() is None:
        return parent_number
    else:
        parent_number = parent_number + 1
        return check_if_parent_exist(item.parent(), parent_number)


def get_buy_simulation_settings(strategy_page):
    buy_simulation_settings = {'buy_settings': []}
    buy_simulation_settings['buy_settings'].append({
        'price_source': strategy_page.buy_price_source_comboBox.currentText(),
        'fee': strategy_page.buy_commission_lineEdit_1.text(),
        'fee_unit': strategy_page.buy_commission_comboBox_2.currentText(),
        'starting_balance': strategy_page.buy_balance_lineEdit2.text()})
    return buy_simulation_settings


def get_sell_simulation_settings(strategy_page):
    sell_simulation_settings = {'sell_settings': []}
    sell_simulation_settings['sell_settings'].append({
        'price_source': strategy_page.sell_price_source_comboBox.currentText(),
        'fee': strategy_page.sell_commission_lineEdit_1.text(),
        'fee_unit': strategy_page.sell_commission_comboBox_2.currentText(),
        'starting_balance': strategy_page.sell_balance_lineEdit.text(),
        'is_stop_loss_selected': strategy_page.stop_loss_checkbox.isChecked(),
        'stop_loss': strategy_page.sell_stop_loss_lineEdit_1.text(),
        'stop_loss_unit': strategy_page.sell_stop_loss_comboBox_2.currentText(),
        'is_take_profit_selected': strategy_page.take_profit_checkbox.isChecked(),
        'take_profit': strategy_page.sell_take_profit_lineEdit_1.text(),
        'take_profit_unit': strategy_page.sell_take_profit_comboBox_2.currentText()})
    return sell_simulation_settings


def check_if_stop_loss_price_is_achieved(x, sell_simulation_settings, trades_dict):
    stop_loss_value = float(sell_simulation_settings['sell_settings'][0]['stop_loss'])
    stop_loss_unit = sell_simulation_settings['sell_settings'][0]['stop_loss_unit']
    if trades_dict['buy_trades'][-1]['index'] > trades_dict['sell_trades'][-1]['index']:
        if stop_loss_unit == '%':
            if data_df.iloc[x]['Low'] <= trades_dict['buy_trades'][-1]['price'] * (100 - stop_loss_value) / 100 <= data_df.iloc[x]['High']:
                sell(x, sell_simulation_settings, trades_dict, trades_dict['buy_trades'][-1]['price'] * (100 - stop_loss_value))
        elif stop_loss_unit == 'Pips':
            if data_df.iloc[x]['Low'] <= trades_dict['buy_trades'][-1]['price'] - (stop_loss_value * pow(10, -pip_position)) <= data_df.iloc[x]['High']:
                sell(x, sell_simulation_settings, trades_dict, trades_dict['buy_trades'][-1]['price'] - (stop_loss_value * pow(10, -pip_position)))
        elif stop_loss_unit == 'Flat':
            if data_df.iloc[x]['Low'] <= trades_dict['buy_trades'][-1]['price'] - stop_loss_value <= data_df.iloc[x]['High']:
                sell(x, sell_simulation_settings, trades_dict, trades_dict['buy_trades'][-1]['price'] - stop_loss_value)


def check_if_take_profit_price_is_achieved(x, sell_simulation_settings, trades_dict):
    take_profit_value = float(sell_simulation_settings['sell_settings'][0]['take_profit'])
    take_profit_unit = sell_simulation_settings['sell_settings'][0]['take_profit_unit']
    if trades_dict['buy_trades'][-1]['index'] > trades_dict['sell_trades'][-1]['index']:
        if data_df.iloc[x]['Low'] <= trades_dict['buy_trades'][-1]['price'] * (100 + take_profit_value) / 100 <= data_df.iloc[x]['High']:
                sell(x, sell_simulation_settings, trades_dict, trades_dict['buy_trades'][-1]['price'] * (100 + take_profit_value) / 100)
        elif take_profit_unit == 'Pips':
            if data_df.iloc[x]['Low'] <= trades_dict['buy_trades'][-1]['price'] + (take_profit_value * pow(10, -pip_position)) <= data_df.iloc[x]['High']:
                sell(x, sell_simulation_settings, trades_dict, trades_dict['buy_trades'][-1]['price'] + (take_profit_value * pow(10, -pip_position)))
        elif take_profit_unit == 'Flat':
            if data_df.iloc[x]['Low'] <= trades_dict['buy_trades'][-1]['price'] + take_profit_value <= data_df.iloc[x]['High']:
                sell(x, sell_simulation_settings, trades_dict, trades_dict['buy_trades'][-1]['price'] + take_profit_value)


def glue_all_code(buy_if_string, sell_if_string, sell_simulation_settings):
    simulation_code = "for x in range(14, len(data_df)):\n"
    if sell_simulation_settings['sell_settings'][0]['is_stop_loss_selected']:
        simulation_code += '\tcheck_if_stop_loss_price_is_achieved(x, sell_simulation_settings, trades_dict)\n'
    if sell_simulation_settings['sell_settings'][0]['is_take_profit_selected']:
        simulation_code += '\tcheck_if_take_profit_price_is_achieved(x, sell_simulation_settings, trades_dict)\n'
    simulation_code += buy_if_string + "\n" + sell_if_string
    return simulation_code


def buy(x, buy_simulation_settings, trades_dict):
    if trades_dict['buy_trades'][-1]['index'] <= trades_dict['sell_trades'][-1]['index'] < x:
        if trades_dict['sell_trades'][-1]['currency_2'] > 0:
            current_price = float(data_df.iloc[x][buy_simulation_settings['buy_settings'][0]['price_source']])
            trades_dict['buy_trades'].append({
                'index': x,
                'price': current_price,
                'amount_traded': trades_dict['sell_trades'][-1]['currency_2'],
                'currency_1': calculate_amount_without_fee('buy',
                                                           current_price, trades_dict['sell_trades'][-1]['currency_2'],
                                                           buy_simulation_settings['buy_settings'][0]['fee'],
                                                           buy_simulation_settings['buy_settings'][0]['fee_unit'])
                              + trades_dict['sell_trades'][-1]['currency_1'],
                'currency_2': 0
            })
        # print('-----------------------------------------------------------------------------------------')
        # print(x, ') BOUGHT ', trades_dict['buy_trades'][-1]['amount_traded'], ' FOR ',  trades_dict['buy_trades'][-1]['price'])


def sell(x, sell_simulation_settings, trades_dict, price='options'):
    if trades_dict['sell_trades'][-1]['index'] <= trades_dict['buy_trades'][-1]['index'] < x:
        if trades_dict['buy_trades'][-1]['currency_1'] > 0:
            if price == 'options':
                current_price = float(data_df.iloc[x][sell_simulation_settings['sell_settings'][0]['price_source']])
            else:
                current_price = float(price)
            trades_dict['sell_trades'].append({
                'index': x,
                'price': current_price,
                'amount_traded': trades_dict['buy_trades'][-1]['currency_1'],
                'currency_1': 0,
                'currency_2': calculate_amount_without_fee('sell',
                                                           current_price, trades_dict['buy_trades'][-1]['currency_1'],
                                                           sell_simulation_settings['sell_settings'][0]['fee'],
                                                           sell_simulation_settings['sell_settings'][0]['fee_unit'])
                              + trades_dict['buy_trades'][-1]['currency_2']
            })
        # if len(trades_dict['buy_trades']) > 1:
        #     print(x, ') SOLD ', trades_dict['sell_trades'][-1]['amount_traded'], ' FOR ', trades_dict['sell_trades'][-1]['price'])
        #     print('***PROFIT: ', trades_dict['buy_trades'][-1]['amount_traded'] - trades_dict['buy_trades'][-2]['amount_traded'])


def calculate_amount_without_fee(context, exchange_rate, currency_amount, fee_value, fee_type):
    fee_value = float(fee_value)
    if fee_type == '%':
        if context == 'buy':
            return (currency_amount / exchange_rate) * (100 - fee_value) / 100
        else:
            return (currency_amount * exchange_rate) * (100 - fee_value) / 100
    elif fee_type == 'Pips':
        if context == 'buy':
            return currency_amount / (exchange_rate + fee_value / 10000)
        else:
            return currency_amount * (exchange_rate - fee_value / 10000)
    elif fee_type == 'Flat':
        if context == 'buy':
            return (currency_amount - fee_value) / exchange_rate
        else:
            return (currency_amount * exchange_rate) - fee_value


def get_pip_position_for_simulation():
    largest_decimal_place = 0
    for index, row in data_df[:int(len(data_df)/4)].iterrows():
        if len(str(row['Open'])) - int(str(row['Open']).find('.')) - 1 > largest_decimal_place:
            largest_decimal_place = len(str(row['Open'])) - int(str(row['Open']).find('.')) - 1
    return largest_decimal_place


def init_simulation(main_window_object, path_to_data):
    buy_rules = get_buy_rules(main_window_object.strategy_page)
    sell_rules = get_sell_rules(main_window_object.strategy_page)
    buy_simulation_settings = get_buy_simulation_settings(main_window_object.strategy_page)
    sell_simulation_settings = get_sell_simulation_settings(main_window_object.strategy_page)
    global data_df
    data_df = pd.read_csv("data/data.csv", sep=';')
    global pip_position
    pip_position = get_pip_position_for_simulation()

    # BUYS
    for x in range(len(buy_rules['buy_rules'])):
        # slice rules to separate usable chunks
        globals()[f"buy_first_indicator_short_name{x}"], globals()[f"buy_first_indicator_options_list{x}"],\
        globals()[f"buy_first_indicator_period{x}"], globals()[f"buy_math_char{x}"],\
        globals()[f"buy_second_indicator_short_name{x}"], globals()[f"buy_second_indicator_options_list{x}"],\
        globals()[f"buy_second_indicator_period{x}"] = slice_rule(buy_rules['buy_rules'][x]['rule_text'])

        # calculate needed indicators and assign them to data_df
        if build_column_name(globals()[f"buy_first_indicator_short_name{x}"], globals()[f"buy_first_indicator_options_list{x}"]) not in data_df.columns:
            data_df = data_df.join(helpers.indicator_function_name[globals()[f"buy_first_indicator_short_name{x}"]](*globals()[f"buy_first_indicator_options_list{x}"]), how='inner')

        if build_column_name(globals()[f"buy_second_indicator_short_name{x}"], globals()[f"buy_second_indicator_options_list{x}"]) not in data_df.columns:
            data_df = data_df.join(helpers.indicator_function_name[globals()[f"buy_second_indicator_short_name{x}"]](*globals()[f"buy_second_indicator_options_list{x}"]), how='inner')

        # build if statement
        buy_rules['buy_rules'][x]['if_statement'] = build_if_statement(globals()[f"buy_first_indicator_short_name{x}"],
                                                              globals()[f"buy_first_indicator_options_list{x}"],
                                                              globals()[f"buy_first_indicator_period{x}"],
                                                              globals()[f"buy_math_char{x}"],
                                                              globals()[f"buy_second_indicator_short_name{x}"],
                                                              globals()[f"buy_second_indicator_options_list{x}"],
                                                              globals()[f"buy_second_indicator_period{x}"])

    # SELLS
    for x in range(len(sell_rules['sell_rules'])):
        # slice rules to separate usable chunks
        globals()[f"sell_first_indicator_short_name{x}"], globals()[f"sell_first_indicator_options_list{x}"], \
        globals()[f"sell_first_indicator_period{x}"], globals()[f"sell_math_char{x}"], \
        globals()[f"sell_second_indicator_short_name{x}"], globals()[f"sell_second_indicator_options_list{x}"], \
        globals()[f"sell_second_indicator_period{x}"] = slice_rule(sell_rules['sell_rules'][x]['rule_text'])

        # calculate needed indicators and assign them to data_df
        if build_column_name(globals()[f"sell_first_indicator_short_name{x}"], globals()[f"sell_first_indicator_options_list{x}"]) not in data_df.columns:
            data_df = data_df.join(helpers.indicator_function_name[globals()[f"sell_first_indicator_short_name{x}"]](*globals()[f"sell_first_indicator_options_list{x}"]), how='inner')

        if build_column_name(globals()[f"sell_second_indicator_short_name{x}"], globals()[f"sell_second_indicator_options_list{x}"]) not in data_df.columns:
            data_df = data_df.join(helpers.indicator_function_name[globals()[f"sell_second_indicator_short_name{x}"]](*globals()[f"sell_second_indicator_options_list{x}"]), how='inner')

        # build if statement
        sell_rules['sell_rules'][x]['if_statement'] = build_if_statement(globals()[f"sell_first_indicator_short_name{x}"],
                                                               globals()[f"sell_first_indicator_options_list{x}"],
                                                               globals()[f"sell_first_indicator_period{x}"],
                                                               globals()[f"sell_math_char{x}"],
                                                               globals()[f"sell_second_indicator_short_name{x}"],
                                                               globals()[f"sell_second_indicator_options_list{x}"],
                                                               globals()[f"sell_second_indicator_period{x}"])

    trades_dict = {'buy_trades': [], 'sell_trades': []}
    trades_dict['buy_trades'].append({
        'index': 0,
        'price': data_df.iloc[0][buy_simulation_settings['buy_settings'][0]['price_source']],
        'amount_traded': 0,
        'currency_1': float(buy_simulation_settings['buy_settings'][0]['starting_balance']),
        'currency_2': float(sell_simulation_settings['sell_settings'][0]['starting_balance'])
    })
    trades_dict['sell_trades'].append({
        'index': 0,
        'price': data_df.iloc[0][sell_simulation_settings['sell_settings'][0]['price_source']],
        'amount_traded': 0,
        'currency_1': float(buy_simulation_settings['buy_settings'][0]['starting_balance']),
        'currency_2': float(sell_simulation_settings['sell_settings'][0]['starting_balance'])
    })
    code = glue_all_code(glue_if_statements(buy_rules['buy_rules'], 'buy'), glue_if_statements(sell_rules['sell_rules'], 'sell'), sell_simulation_settings)
    # print(code)
    exec(code)
    print(json.dumps(trades_dict, indent=4))

    # pass and display data in summary_page
    # main_window_object.summary_page.plot_candle_chart()
    main_window_object.summary_page.format_and_dislay_text(trades_dict)