from PySide2 import QtCore
import helpers
import pandas as pd


def get_buy_rules(main_window_object):
    list_of_items_in_buy_and_text = [[]]
    list_of_items_in_buy_qtreewidget = main_window_object.strategy_page.p2_buyCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
    for buy_item in list_of_items_in_buy_qtreewidget:
        list_of_items_in_buy_and_text.append([buy_item, buy_item.text(0), buy_item.parent()])
    return list_of_items_in_buy_and_text[1:]


def get_sell_rules(main_window_object):
    list_of_items_in_sell_and_text = [[]]
    list_of_items_in_sell_qtreewidget = main_window_object.strategy_page.p2_sellCondition_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
    for sell_item in list_of_items_in_sell_qtreewidget:
        list_of_items_in_sell_and_text.append([sell_item, sell_item.text(0), sell_item.parent()])
    return list_of_items_in_sell_and_text[1:]


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

    first_indicator_options = first_indicator_options[1:-1]
    first_indicator_options_list = []
    buy_coma_count = first_indicator_options.count(',')
    if buy_coma_count == 0:
        first_indicator_options_list.append(first_indicator_options)
    else:
        for coma in range(buy_coma_count):
            first_indicator_options_list.append(first_indicator_options[:first_indicator_options.find(',')])
            first_indicator_options = first_indicator_options[first_indicator_options.find(',')+2:]
            if coma == buy_coma_count-1:
                first_indicator_options_list.append(first_indicator_options)

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

    return first_indicator_short_name, first_indicator_options_list, first_indicator_period, math_char,\
           second_indicator_short_name, second_indicator_options_list, second_indicator_period


def build_column_name(indicator_short_name, indicator_options_list):
    combined_column_name = ''
    if indicator_short_name == 'BOLL - Upper Band':
        combined_column_name = 'BOLL_Upper'
    elif indicator_short_name == 'BOLL - Lower Band':
        combined_column_name = 'BOLL_Lower'
    elif indicator_short_name == 'MACD - MACD Line':
        combined_column_name = 'MACD_Line'
    elif indicator_short_name =='MACD - Singal Line':
        combined_column_name = 'MACD_Signal_Line'
    else:
        combined_column_name = indicator_short_name

    for element in indicator_options_list:
        combined_column_name += '_' + element

    return combined_column_name


def build_if_statement(first_indicator_short_name, first_indicator_options_list, first_indicator_period,
                       math_char,
                       second_indicator_short_name, second_indicator_options_list, second_indicator_period):
    first_indicator_collumn_name = build_column_name(first_indicator_short_name, first_indicator_options_list)
    second_indicator_collumn_name = build_column_name(second_indicator_short_name, second_indicator_options_list)
    first_indicator_period = first_indicator_period[1:-1]   # remove square bracket
    second_indicator_period = second_indicator_period[1:-1] # remove square bracket
    if_statement = "if data_df.iloc[x"+first_indicator_period+"]['"+first_indicator_collumn_name+"'] "+math_char+" data_df.iloc[x"+second_indicator_period+"]['"+second_indicator_collumn_name+"']:"
    return if_statement


def glue_if_statements(list_of_rules, context):
    if_statement = "for x in range(len(data_df)):\n"
    for x in range(len(list_of_rules)):
        if_statement += "\t" * (check_if_parent_exist(list_of_rules[x][0], 0) + 1) + list_of_rules[x][3] + "\n"
        if len(list_of_rules) > x+1:
            if check_if_parent_exist(list_of_rules[x][0], 0) >= check_if_parent_exist(list_of_rules[x+1][0], 0):
                if_statement += "\t" * (check_if_parent_exist(list_of_rules[x][0], 0) + 2) + context + "()\n"
        else:
            if_statement += "\t" * (check_if_parent_exist(list_of_rules[x][0], 0) + 2) + context + "()\n"

    return if_statement

# helper function to glue_if_statements()
def check_if_parent_exist(item, parent_number):
    if item.parent() is None:
        return parent_number
    else:
        parent_number = parent_number + 1
        return check_if_parent_exist(item.parent(), parent_number)


def init_simulation(main_window_object):
    buy_rules = get_buy_rules(main_window_object)
    sell_rules = get_sell_rules(main_window_object)
    global data_df
    data_df = pd.read_csv("data/data.csv", sep=';')

    # BUYS
    for x in range(len(buy_rules)):
        # slice rules to separate usable chunks
        globals()[f"buy_first_indicator_short_name{x}"], globals()[f"buy_first_indicator_options_list{x}"],\
        globals()[f"buy_first_indicator_period{x}"], globals()[f"buy_math_char{x}"],\
        globals()[f"buy_second_indicator_short_name{x}"], globals()[f"buy_second_indicator_options_list{x}"],\
        globals()[f"buy_second_indicator_period{x}"] = slice_rule(buy_rules[x][1])

        # calculate needed indicators and assign them to data_df
        if build_column_name(globals()[f"buy_first_indicator_short_name{x}"], globals()[f"buy_first_indicator_options_list{x}"]) not in data_df.columns:
            data_df = data_df.join(helpers.indicator_function_name[globals()[f"buy_first_indicator_short_name{x}"]](*globals()[f"buy_first_indicator_options_list{x}"]), how='inner')

        if build_column_name(globals()[f"buy_second_indicator_short_name{x}"], globals()[f"buy_second_indicator_options_list{x}"]) not in data_df.columns:
            data_df = data_df.join(helpers.indicator_function_name[globals()[f"buy_second_indicator_short_name{x}"]](*globals()[f"buy_second_indicator_options_list{x}"]), how='inner')

        # build if statement
        globals()[f"buy_if_statement{x}"] = build_if_statement(globals()[f"buy_first_indicator_short_name{x}"],
                                                              globals()[f"buy_first_indicator_options_list{x}"],
                                                              globals()[f"buy_first_indicator_period{x}"],
                                                              globals()[f"buy_math_char{x}"],
                                                              globals()[f"buy_second_indicator_short_name{x}"],
                                                              globals()[f"buy_second_indicator_options_list{x}"],
                                                              globals()[f"buy_second_indicator_period{x}"])
        buy_rules[x].append(globals()[f"buy_if_statement{x}"])

    # SELLS
    for x in range(len(sell_rules)):
        # slice rules to separate usable chunks
        globals()[f"sell_first_indicator_short_name{x}"], globals()[f"sell_first_indicator_options_list{x}"], \
        globals()[f"sell_first_indicator_period{x}"], globals()[f"sell_math_char{x}"], \
        globals()[f"sell_second_indicator_short_name{x}"], globals()[f"sell_second_indicator_options_list{x}"], \
        globals()[f"sell_second_indicator_period{x}"] = slice_rule(sell_rules[x][1])

        # calculate needed indicators and assign them to data_df
        if build_column_name(globals()[f"sell_first_indicator_short_name{x}"], globals()[f"sell_first_indicator_options_list{x}"]) not in data_df.columns:
            data_df = data_df.join(helpers.indicator_function_name[globals()[f"sell_first_indicator_short_name{x}"]](*globals()[f"sell_first_indicator_options_list{x}"]), how='inner')

        if build_column_name(globals()[f"sell_second_indicator_short_name{x}"], globals()[f"sell_second_indicator_options_list{x}"]) not in data_df.columns:
            data_df = data_df.join(helpers.indicator_function_name[globals()[f"sell_second_indicator_short_name{x}"]](*globals()[f"sell_second_indicator_options_list{x}"]), how='inner')

        # build if statement
        globals()[f"sell_if_statement{x}"] = build_if_statement(globals()[f"sell_first_indicator_short_name{x}"],
                                                               globals()[f"sell_first_indicator_options_list{x}"],
                                                               globals()[f"sell_first_indicator_period{x}"],
                                                               globals()[f"sell_math_char{x}"],
                                                               globals()[f"sell_second_indicator_short_name{x}"],
                                                               globals()[f"sell_second_indicator_options_list{x}"],
                                                               globals()[f"sell_second_indicator_period{x}"])
        sell_rules[x].append(globals()[f"sell_if_statement{x}"])

    print(glue_if_statements(buy_rules, 'buy'))
    print(glue_if_statements(sell_rules, 'sell'))