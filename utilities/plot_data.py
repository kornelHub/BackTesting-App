import plotly.graph_objects as go
import plotly.offline as plt
from plotly.subplots import make_subplots
import engine.calculate_indicators as calculate_indicators
from engine.simulation import build_column_name
from engine.simulation import get_pip_position_for_simulation
from utilities.helpers import return_index_of_first_non_zero_row
from operator import itemgetter
import numpy as np


def plot_ohlcv_data(ohlcv_data):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=ohlcv_data['Opentime'], open=ohlcv_data['Open'], high=ohlcv_data['High'],
                                 low=ohlcv_data['Low'], close=ohlcv_data['Close']))
    fig.update_layout(xaxis_rangeslider_visible=False, yaxis_tickformat = f".{get_pip_position_for_simulation(ohlcv_data)}f")
    html = '<html><body>'
    html += plt.plot(fig, output_type='div', include_plotlyjs='cdn')
    html += '</body></html>'
    return html

def plot_balance(fig, trades_dict, list_of_profit):
    index_list = []
    global balance_list
    balance_list = []
    for x in list_of_profit:
        index_list.append(x[0])
        balance_list.append(x[1])

    buys_indexes = list(map(itemgetter('index'), trades_dict['buy_trades']))[1:]
    buys_amount_in_currency_2 = np.multiply(list(map(itemgetter('currency_1'), trades_dict['buy_trades'])),
                                            list(map(itemgetter('price'), trades_dict['buy_trades'])))[1:]
    buys_id_rule = list(map(itemgetter('id_rule'), trades_dict['buy_trades']))[1:]

    sells_indexes = list(map(itemgetter('index'), trades_dict['sell_trades']))[1:]
    sells_amount_in_currency_2 = list(map(itemgetter('currency_2'), trades_dict['sell_trades']))[1:]
    sells_id_rule = list(map(itemgetter('id_rule'), trades_dict['sell_trades']))[1:]

    fig.add_trace(go.Scatter(mode='lines', x=index_list, y=balance_list, name='Account', marker=dict(color='LightSeaGreen')), row=1, col=1)
    fig.add_shape(type='line', x0=0, y0=balance_list[0], x1=index_list[-1], y1=balance_list[0], line=dict(color='black', dash='dot'), row=1, col=1)
    fig.add_trace(go.Scatter(mode='markers', x=sells_indexes, y=sells_amount_in_currency_2, text=sells_id_rule,
                             hovertemplate='<i>Transaction ID: </i>%{x}<br>'+'<i>Balance: </i>%{y}<br>'+'<i>Rule ID: </i>%{text}<br>',
                             marker=dict(color='brown', size=8), name='Sell transaction'), row=1, col=1)
    fig.add_trace(go.Scatter(mode='markers', x=buys_indexes, y=buys_amount_in_currency_2, text=buys_id_rule,
                             hovertemplate='<i>Transaction ID: </i>%{x}<br>'+'<i>Balance: </i>%{y}<br>'+'<i>Rule ID: </i>%{text}<br>',
                             marker=dict(color='royalblue', size = 8), name='Buy transaction'), row=1, col=1)
    return fig

def plot_ohlc_data_with_transactions(fig, ohlcv_data, trades_dict):
    sells_indexes = list(map(itemgetter('index'), trades_dict['sell_trades']))[1:]
    sells_price = list(map(itemgetter('price'), trades_dict['sell_trades']))[1:]
    sells_id_rule = list(map(itemgetter('id_rule'), trades_dict['sell_trades']))[1:]

    buys_indexes = list(map(itemgetter('index'), trades_dict['buy_trades']))[1:]
    buys_price = list(map(itemgetter('price'), trades_dict['buy_trades']))[1:]
    buys_id_rule = list(map(itemgetter('id_rule'), trades_dict['buy_trades']))[1:]

    fig.add_trace(go.Candlestick(x=ohlcv_data.index, open=ohlcv_data['Open'], high=ohlcv_data['High'],
                                 low=ohlcv_data['Low'], close=ohlcv_data['Close']), row=2, col=1)
    fig.add_trace(go.Scatter(mode='markers', x=sells_indexes, y=sells_price, text=sells_id_rule,
                             hovertemplate='<i>Transaction ID: </i>%{x}<br>' + '<i>Price: </i>%{y}<br>' + '<i>Rule ID: </i>%{text}<br>',
                             marker=dict(color='brown', size=8),name='Sell transaction'), row=2, col=1)
    fig.add_trace(go.Scatter(mode='markers', x=buys_indexes, y=buys_price, text=buys_id_rule,
                             hovertemplate='<i>Transaction ID: </i>%{x}<br>' + '<i>Price: </i>%{y}<br>' + '<i>Rule ID: </i>%{text}<br>',
                             marker=dict(color='royalblue', size = 8),name='Buy transaction'), row=2, col=1)
    return fig

def plot_ohlc_and_balance_with_transactions(ohlcv_data, trades_dict, list_of_profit, currency_2_symbol):
    fig = make_subplots(rows=2, cols= 1, shared_xaxes=True, row_heights=[800, 800],
                        subplot_titles=("title_1_to_change", "OHLC data"),vertical_spacing=0.05)
    fig = plot_balance(fig, trades_dict, list_of_profit)
    fig.update_layout(yaxis_tickformat=f".{get_pip_position_for_simulation(ohlcv_data)}f")
    fig = plot_ohlc_data_with_transactions(fig, ohlcv_data, trades_dict)
    fig.update_yaxes(tickformat=f".{get_pip_position_for_simulation(ohlcv_data)}f")
    fig.layout.annotations[0].update(text="Total profit: {} {}".format(balance_list[-1] - balance_list[0], currency_2_symbol))
    html = '<html><body>'
    html += plt.plot(fig, output_type='div', include_plotlyjs='cdn')
    html += '</body></html>'
    return html


def plot_ohlcv_with_indicators(ohlcv_data, list_with_indicators):
    calculate_indicators.read_ohlcv_from_file()
    for x in range(len(list_with_indicators)):
        # make short of indicators
        list_with_indicators[x].append(list_with_indicators[x][0][: list_with_indicators[x][0].find('(')-1])

        # convert indicators options to list
        if list_with_indicators[x][1] != '(-)':
            list_with_indicators[x][1] = [list_with_indicators[x][1][1:-1].split(', ')][0]
        else:
            list_with_indicators[x][1] = []

        if build_column_name(list_with_indicators[x][2], list_with_indicators[x][1]) not in ohlcv_data.columns:
            list_with_indicators[x].append(build_column_name(list_with_indicators[x][2], list_with_indicators[x][1]))
            ohlcv_data = ohlcv_data.join(calculate_indicators.indicator_function_name[list_with_indicators[x][2]](*list_with_indicators[x][1]), how='inner')

    # calculate needed subplots
    list_with_indicators, needed_subplots  = calculate_needed_subplots(list_with_indicators)
    ohlcv_data = ohlcv_data[return_index_of_first_non_zero_row(ohlcv_data):]
    print(needed_subplots)
    plots_size = [0.5]
    for x in range(needed_subplots-2):
        plots_size.append((1 - plots_size[0]) / needed_subplots)

    fig = make_subplots(rows=needed_subplots-1, cols= 1, shared_xaxes=True, row_heights=plots_size, vertical_spacing=0.01)
    fig.add_trace(go.Candlestick(x=ohlcv_data['Opentime'], open=ohlcv_data['Open'], high=ohlcv_data['High'],
                                 low=ohlcv_data['Low'], close=ohlcv_data['Close']), row=1, col=1)

    for x in list_with_indicators:
        if is_indicator_need_subplot(x[2]):
            fig.add_trace(go.Scatter(mode='lines', x=ohlcv_data['Opentime'], y=ohlcv_data[x[3]], name=x[3]), row=x[4], col=1)
        else:
            if x[2] != 'SAR':
                fig.add_trace(go.Scatter(mode='lines', x=ohlcv_data['Opentime'], y=ohlcv_data[x[3]], name=x[3]), row=1, col=1)
            else:
                fig.add_trace(go.Scatter(mode='markers', x=ohlcv_data['Opentime'], y=ohlcv_data[x[3]], name=x[3]), row=1,col=1)

    fig.update_layout(xaxis_rangeslider_visible=False, hovermode="x unified", yaxis_tickformat = f".{get_pip_position_for_simulation(ohlcv_data)}f")
    html = '<html><body>'
    html += plt.plot(fig, output_type='div', include_plotlyjs='cdn')
    html += '</body></html>'
    return html


def calculate_needed_subplots(list_with_indicators):
    counter = 2
    for x in range(len(list_with_indicators)):
        if is_indicator_need_subplot(list_with_indicators[x][2]):
            if 'MACD' in list_with_indicators[x][2]:  # check if there are two MACD line and sinnal line with the same options
                for y in range(0, x):
                    if list_with_indicators[x][1] == list_with_indicators[y][1]:
                        list_with_indicators[x].append(list_with_indicators[y][4])
                    elif x - 1 == y:
                        list_with_indicators[x].append(counter)
                        counter += 1

            else:
                list_with_indicators[x].append(counter)
                counter += 1
        else:
            list_with_indicators[x].append(1)
    return list_with_indicators, counter


def is_indicator_need_subplot(indicator):
    subplots_indicator = ['MACD - MACD Line', 'MACD - Singal Line', 'RSI', 'KDJ', 'OBV', 'CCI', 'StochRSI', 'WR', 'DMI', 'MTM', 'EVM']
    return indicator in subplots_indicator