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

def transform_if_needed(indicator_option):
    if indicator_option == 'Open' or indicator_option == 'High' or indicator_option == 'Low' or indicator_option == 'Close':
        return indicator_option
    else:
        return int(indicator_option)


def init_simulation(main_window_object):
    buy_rules = get_buy_rules(main_window_object)
    sell_rules = get_sell_rules(main_window_object)
    data_df = pd.read_csv("data/data.csv", sep=';')

    # slice rules to separate chunks
    for x in range(len(buy_rules)):
        globals()[f"buy_first_indicator_short_name{x}"], globals()[f"buy_first_indicator_options_list{x}"],\
        globals()[f"buy_first_indicator_period{x}"],globals()[f"buy_math_char{x}"],\
        globals()[f"buy_second_indicator_short_name{x}"], globals()[f"buy_second_indicator_options_list{x}"],\
        globals()[f"buy_second_indicator_period{x}"] = slice_rule(buy_rules[x][1])

    for x in range(len(sell_rules)):
        globals()[f"sell_first_indicator_short_name{x}"], globals()[f"sell_first_indicator_options_list{x}"], \
        globals()[f"sell_first_indicator_period{x}"], globals()[f"sell_math_char{x}"], \
        globals()[f"sell_second_indicator_short_name{x}"], globals()[f"sell_second_indicator_options_list{x}"], \
        globals()[f"sell_second_indicator_period{x}"] = slice_rule(sell_rules[x][1])

    data_df = data_df.join(helpers.indicator_function_name[buy_first_indicator_short_name0](pd.read_csv("data/data.csv", sep=';'), transform_if_needed(buy_first_indicator_options_list0[0]), transform_if_needed(buy_first_indicator_options_list0[1])), how='inner')
    print(data_df.to_string())