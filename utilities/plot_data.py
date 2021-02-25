import pandas as pd
import plotly.graph_objects as go
import plotly.offline as plt


def plot_ohlcv_data(path_to_file):
    ohlcv_data = pd.read_csv(path_to_file, skiprows=[0], sep=';')
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=ohlcv_data['Opentime'], open=ohlcv_data['Open'], high=ohlcv_data['High'],
                                 low=ohlcv_data['Low'], close=ohlcv_data['Close']))
    fig.update_layout(xaxis_rangeslider_visible=False)
    html = '<html><body>'
    html += plt.plot(fig, output_type='div', include_plotlyjs='cdn')
    html += '</body></html>'
    return html

def plot_balance(list_of_profit, starting_balance, currency_2_symbol):
    print(starting_balance)
    index_list = []
    balance_list = []
    for x in list_of_profit:
        index_list.append(x[0])
        balance_list.append(x[1])

    fig = go.Figure(
        data=[go.Scatter(y=balance_list, x=index_list)],
        layout_title_text="Total profit: {} {}".format(balance_list[-1] - starting_balance, currency_2_symbol))
    html = '<html><body>'
    html += plt.plot(fig, output_type='div', include_plotlyjs='cdn')
    html += '</body></html>'
    return html