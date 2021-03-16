import pandas as pd
import plotly.graph_objects as go
import plotly.offline as plt
import engine.calculate_indicators as calculate_indicators
from engine.simulation import build_column_name


def plot_ohlcv_data(ohlcv_data):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=ohlcv_data['Opentime'], open=ohlcv_data['Open'], high=ohlcv_data['High'],
                                 low=ohlcv_data['Low'], close=ohlcv_data['Close']))
    fig.update_layout(xaxis_rangeslider_visible=False)
    html = '<html><body>'
    html += plt.plot(fig, output_type='div', include_plotlyjs='cdn')
    html += '</body></html>'
    return html

def plot_balance(list_of_profit, currency_2_symbol):
    index_list = []
    balance_list = []
    for x in list_of_profit:
        index_list.append(x[0])
        balance_list.append(x[1])

    fig = go.Figure(
        data=[go.Scatter(y=balance_list, x=index_list)],
        layout_title_text="Total profit: {} {}".format(balance_list[-1] - balance_list[0], currency_2_symbol))
    fig.add_shape(type='line', x0=0, y0=balance_list[0], x1=index_list[-1], y1=balance_list[0],
                  line=dict(color='LightSeaGreen', dash='dot'))
    html = '<html><body>'
    html += plt.plot(fig, output_type='div', include_plotlyjs='cdn')
    html += '</body></html>'
    return html

def plot_ohlcv_with_indicators(ohlcv_data, list_with_indicators):
    calculate_indicators.read_ohlcv_from_file()
    for x in range(len(list_with_indicators)):
        # make short of indicators
        list_with_indicators[x][0] = list_with_indicators[x][0][: list_with_indicators[x][0].find('(')-1]

        # convert indicators options to list
        if list_with_indicators[x][1] != '(-)':
            list_with_indicators[x][1] = [list_with_indicators[x][1][1:-1].split(', ')][0]
        else:
            list_with_indicators[x][1] = []

        if build_column_name(list_with_indicators[x][0], list_with_indicators[x][1]) not in ohlcv_data.columns:
            print(list_with_indicators[x][1])
            ohlcv_data = ohlcv_data.join(calculate_indicators.indicator_function_name[list_with_indicators[x][0]](*list_with_indicators[x][1]), how='inner')

    print(ohlcv_data.to_string())

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=ohlcv_data['Opentime'], open=ohlcv_data['Open'], high=ohlcv_data['High'],
                                 low=ohlcv_data['Low'], close=ohlcv_data['Close']))
    fig.update_layout(xaxis_rangeslider_visible=False)
    html = '<html><body>'
    html += plt.plot(fig, output_type='div', include_plotlyjs='cdn')
    html += '</body></html>'
    return html