import pandas as pd
import plotly.graph_objects as go
import plotly.offline as plt

def plot_ohlcv_data(path_to_file):
    ohlcv_data = pd.read_csv(path_to_file, sep=';')
    print(ohlcv_data)

    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=ohlcv_data['Opentime'], open=ohlcv_data['Open'], high=ohlcv_data['High'], low=ohlcv_data['Low'], close=ohlcv_data['Close']))
    fig.update_layout(xaxis_rangeslider_visible=False)
    # fig.write_image('data/temporary_plot.png')
    html = '<html><body>'
    html += plt.plot(fig, output_type='div', include_plotlyjs='cdn')
    html += '</body></html>'
    return html