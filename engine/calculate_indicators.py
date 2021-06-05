import pandas as pd
import numpy as np
from utilities.helpers import load_ohlcv_data_from_csv_file

global data_df

def read_ohlcv_from_file():
    global data_df
    data_df = load_ohlcv_data_from_csv_file()

def simple_moving_average(period, source):
    period = int(period)
    if source == 'typical_price':
        answer_df = pd.DataFrame(data_df[['High', 'Low', 'Close']], columns=['High', 'Low', 'Close'])
        answer_df['typical_price'] = answer_df.mean(axis=1)
        answer_df = answer_df.drop(columns=['High', 'Low', 'Close'])
    else:
        answer_df = pd.DataFrame(data_df[source], columns=[source])
    answer_df['sma'] = 0
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np - 1)):
        answer_np[x][1] = np.mean(answer_np[x - period + 1:x + 1, 0])

    if source == 'typical_price':
        return pd.DataFrame(answer_np, columns=[['typical_price', 'sma_of_typical_price']])
    else:
        return pd.DataFrame(answer_np[:, 1], columns=['SMA_{}_{}'.format(period, source)])


def exponential_moving_average(period, source):
    period = int(period)
    ema_multiplier = 2 / (period + 1)
    answer_df = pd.DataFrame(data_df[source], columns=[source])
    answer_df['ema'] = 0

    # source[0], ema[1]
    answer_np = answer_df.to_numpy()
    # find first [period] not zero values, helps in other indicator
    y = 0
    while y <= len(answer_np):
        if 0 in answer_np[y:y + period, 0]:
            y += 1
        else:
            break

    answer_np[period - 1 + y, 1] = np.mean(answer_np[0 + y:period + y, 0])
    for x in range(period + y, len(answer_np - 1)):
        answer_np[x][1] = (answer_np[x][0] * ema_multiplier) + answer_np[x - 1][1] * (1 - ema_multiplier)

    return pd.DataFrame(answer_np[:, 1], columns=['EMA_{}_{}'.format(period, source)])


def exponential_moving_average_helper(data_df, period, source):
    period = int(period)
    ema_multiplier = 2 / (period + 1)
    answer_df = pd.DataFrame(data_df[source], columns=[source])
    answer_df['ema'] = 0

    # source[0], ema[1]
    answer_np = answer_df.to_numpy()
    # find first [period] not zero values, helps in other indicator
    y = 0
    while y <= len(answer_np):
        if 0 in answer_np[y:y + period, 0]:
            y += 1
        else:
            break

    answer_np[period - 1 + y, 1] = np.mean(answer_np[0 + y:period + y, 0])
    for x in range(period + y, len(answer_np - 1)):
        answer_np[x][1] = (answer_np[x][0] * ema_multiplier) + answer_np[x - 1][1] * (1 - ema_multiplier)
    return answer_np


def weighted_moving_average(period, source):
    period = int(period)
    answer_df = pd.DataFrame(data_df[source], columns=[source])
    answer_df['wma'] = 0
    # source[0], wma[1]
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np - 1)):
        weighted_sum, divider = 0, 0
        for y in range(1, period + 1):
            weighted_sum += answer_np[x + 1 - y, 0] * (period + 1 - y)
            divider += y
        answer_np[x][1] = weighted_sum / divider
    return pd.DataFrame(answer_np[:, 1], columns=['WMA_{}_{}'.format(period, source)])


def bollinger_band_upper(period, multiplier):
    period = int(period)
    multiplier = int(multiplier)
    # High_Low_Close_SMA, High_Low_Close_SMA_period_SMA
    answer_df = simple_moving_average(period, 'typical_price')
    answer_df['standard_deviation'] = 0
    answer_df['bollinger_band_upper'] = 0

    # typical_price[0], sma_of_typical_price[1], standard_deviation[2], bollinger_band_upper[3]
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np)):
        # standard_deviation assign
        answer_np[x, 2] = np.std(answer_np[x + 1 - period:x + 1, 0], axis=0, dtype=np.float64)
        # bollinger_band_upper assign
        answer_np[x, 3] = answer_np[x, 1] + (answer_np[x, 2] * multiplier)

    return pd.DataFrame(answer_np[:, 3], columns=['BOLL_Upper_{}_{}'.format(period, multiplier)])


def bollinger_band_lower(period, multiplier):
    period = int(period)
    multiplier = int(multiplier)
    # High_Low_Close_SMA, High_Low_Close_SMA_period_SMA
    answer_df = simple_moving_average(period, 'typical_price')
    answer_df['standard_deviation'] = 0
    answer_df['bollinger_band_lower'] = 0

    # typical_price[0], sma_of_typical_price[1], standard_deviation[2], bollinger_band_lower[3]
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np)):
        # standard_deviation assign
        answer_np[x, 2] = np.std(answer_np[x + 1 - period:x + 1, 0], axis=0, dtype=np.float64)
        # bollinger_band_upper assign
        answer_np[x, 3] = answer_np[x, 1] - (answer_np[x, 2] * multiplier)

    return pd.DataFrame(answer_np[:, 3], columns=['BOLL_Lower_{}_{}'.format(period, multiplier)])


def volume_weighted_average_price(period):
    # https://www.investopedia.com/articles/trading/11/trading-with-vwap-mvwap.asp
    answer_df = pd.DataFrame(data_df[['High', 'Low', 'Close', 'Volume']], columns=['High', 'Low', 'Close', 'Volume'])
    answer_df[['typical_price', 'tp*v', 'cumulative_tp*v', 'cumulative_volume', 'vwap']] = 0

    # 'High'[0], 'Low'[1], 'Close'[2], 'Volume'[3], typical_price'[4], tp*v[5],
    # cumulative_tp*v[6], 'cumulative_volume'[7], 'vwap'[8]
    period = int(period)
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np)):
        answer_np[x][4] = (answer_np[x][0] + answer_np[x][1] + answer_np[x][2]) / 3
        answer_np[x][5] = answer_np[x][4] * answer_np[x][3]
        answer_np[x][6] = sum(answer_np[x - period + 1:x + 1, 5])
        answer_np[x][7] = sum(answer_np[x - period + 1:x + 1, 3])
        answer_np[x][8] = answer_np[x][6] / answer_np[x][7]
    return pd.DataFrame(answer_np[:, 8], columns=['VWAP_{}'.format(period)])


def trix(period):
    period = int(period)
    answer_df = pd.DataFrame(exponential_moving_average_helper(data_df, period, 'Close'), columns=['Open', '1st_ema'])
    answer_df[['2nd_ema', '3rd_ema']] = 0
    answer_df['2nd_ema'] = exponential_moving_average_helper(answer_df, period, '1st_ema')[:, 1]
    answer_df['3rd_ema'] = exponential_moving_average_helper(answer_df, period, '2nd_ema')[:, 1]
    answer_df['trix'] = 0

    # 3rd_ema[3], trix[4]
    answer_np = answer_df[['3rd_ema', 'trix']].to_numpy()
    for x in range((period * 3) - 2, len(answer_np)):
        answer_np[x, 1] = (answer_np[x, 0] - answer_np[x - 1, 0]) / answer_np[x - 1, 0]
    return pd.DataFrame(answer_np[:, 1], columns=['TRIX_' + str(period)])


def sar(start, maximum):
    start = float(start)
    maximum = float(maximum)
    answer_df = pd.DataFrame(data_df[['Open', 'High', 'Low', 'Close']], columns=['High', 'Low'])
    answer_df[['psar', 'ep', 'acc_factor', '(ep-sar) * acc_factor']] = 0
    answer_df['is_trend_rising'] = ''

    #init first values
    answer_df.at[0, 'psar'] = answer_df.iloc[0]['Low']
    answer_df.at[0, 'ep'] = answer_df.iloc[0]['High']
    answer_df.at[0, 'acc_factor'] = start
    answer_df.at[0, '(ep-sar) * acc_factor'] = (answer_df.iloc[0]['ep'] - answer_df.iloc[0]['psar']) \
                                               * answer_df.iloc[0]['acc_factor']
    answer_df.at[0, 'is_trend_rising'] = True

    # High[0], Low[1], psar[2], ep[3], acc_factor[4], [ep-sar] * acc_factor[5], is_trend_rising[6]
    answer_np = answer_df.to_numpy()
    for x in range(1, len(answer_np)):
        if answer_np[x - 1][6] is True:
            if answer_np[x - 1][2] + answer_np[x - 1][5] > answer_np[x][1]:
                answer_np[x][2] = answer_np[x - 1][3]
            else:
                answer_np[x][2] = answer_np[x - 1][2] + answer_np[x - 1][5]
        else:
            if answer_np[x - 1][2] + answer_np[x - 1][5] < answer_np[x][0]:
                answer_np[x][2] = answer_np[x - 1][3]
            else:
                answer_np[x][2] = answer_np[x - 1][2] + answer_np[x - 1][5]

        # calculate is_trend_rising
        if answer_np[x][2] < answer_np[x][0]:
            answer_np[x][6] = True
        elif answer_np[x][2] > answer_np[x][1]:
            answer_np[x][6] = False

        # calculate acc_factor
        if answer_np[x][6] == answer_np[x - 1][6]:
            if answer_np[x - 1][4] == maximum:
                answer_np[x][4] = maximum
            else:
                if answer_np[x][6] is True:
                    if answer_np[x][3] > answer_np[x - 1][3]:
                        answer_np[x][4] = answer_np[x - 1][4] + start
                    else:
                        answer_np[x][4] = answer_np[x - 1][4]
                else:
                    if answer_np[x][3] < answer_np[x - 1][3]:
                        answer_np[x][4] = answer_np[x - 1][4] + start
                    else:
                        answer_np[x][4] = answer_np[x - 1][4]
        else:
            answer_np[x][4] = start

        # calculate ep 
        if answer_np[x][6] is True:
            if answer_np[x][0] > answer_np[x - 1][3]:
                answer_np[x][3] = answer_np[x][0]
            else:
                answer_np[x][3] = answer_np[x - 1][3]
        else:
            if answer_np[x][1] < answer_np[x - 1][3]:
                answer_np[x][3] = answer_np[x][1]
            else:
                answer_np[x][3] = answer_np[x - 1][3]

        answer_np[x][5] = (answer_np[x][3] - answer_np[x][2]) * answer_np[x][4]

    return pd.DataFrame(answer_np[:,2], columns=['SAR_{}_{}'.format(start,maximum)])

def macd_line(period_1, period_2, period_3, source):
    period_1 = int(period_1)
    period_2 = int(period_2)
    period_3 = int(period_3)
    answer_df = pd.DataFrame(data_df[source], columns=[source])
    answer_df['first_period_ema'] = exponential_moving_average_helper(answer_df, period_1, source)[:, 1]
    answer_df['second_period_ema'] = exponential_moving_average_helper(answer_df, period_2, 'first_period_ema')[:, 1]
    answer_df.loc[answer_df['second_period_ema'] == 0, 'MACD'] = 0
    answer_df.loc[answer_df['second_period_ema'] != 0, 'MACD'] = answer_df['first_period_ema'] - answer_df[
        'second_period_ema']
    answer_df = answer_df.rename(
        columns={'MACD': 'MACD_Line_{}_{}_{}_{}'.format(period_1, period_2, period_3, source)})
    # print(answer_df.to_string())
    return answer_df.iloc[:, 3]


def macd_signal_line(period_1, period_2, period_3, source):
    period_1 = int(period_1)
    period_2 = int(period_2)
    period_3 = int(period_3)
    answer_df = pd.DataFrame(data_df[source], columns=[source])
    answer_df['first_period_ema'] = exponential_moving_average_helper(answer_df, period_1, source)[:, 1]
    answer_df['second_period_ema'] = exponential_moving_average_helper(answer_df, period_2, 'first_period_ema')[:, 1]
    answer_df.loc[answer_df['second_period_ema'] == 0, 'MACD'] = 0
    answer_df.loc[answer_df['second_period_ema'] != 0, 'MACD'] = answer_df['first_period_ema'] - answer_df[
        'second_period_ema']
    answer_df['third_period_ema_of_MACD'] = exponential_moving_average_helper(answer_df, period_3, 'MACD')[:, 1]
    answer_df = answer_df.rename(
        columns={'third_period_ema_of_MACD': 'MACD_Signal_Line_{}_{}_{}_{}'.format(period_1, period_2, period_3, source)})
    return answer_df.iloc[:, 4]


def rsi(period):
    period = int(period)
    answer_df = pd.DataFrame(data_df['Close'], columns=['Close'])
    answer_df[['close_price_change', 'average_gain', 'average_loss', 'rsi']] = 0

    # Close[0], close_price_change[1], average_gain[2], average_loss[3], rsi[4]
    answer_np = answer_df.to_numpy()
    for x in range(1, len(data_df)):
        answer_np[x, 1] = answer_np[x, 0] / answer_np[x - 1, 0]

    for x in range(period, len(answer_np)):
        average_gain = 0
        average_loss = 0
        for y in range(x - period, x + 1):
            if answer_np[y, 1] > 1:
                average_gain += answer_np[y, 1]
            elif answer_np[y, 1] <= 1:
                average_loss += answer_np[y, 1]

        if average_gain == 0:
            answer_np[x, 2] = 0
        else:
            answer_np[x, 2] = average_gain / period

        if average_loss == 0:
            answer_np[x, 3] = 0
        else:
            answer_np[x, 3] = average_loss / period
        answer_np[x, 4] = 100 - (100 / (1 + (answer_np[x, 2] / answer_np[x, 3])))
    answer_df = pd.DataFrame(answer_np[:, 4], columns=['RSI_' + str(period)])
    return answer_df


# TODO see how to use k_smooth and d_smooth
def kdj(period, k_smooth, d_smooth):
    period = int(period)
    k_smooth = int(k_smooth)
    d_smooth = int(d_smooth)
    answer_df = pd.DataFrame(data_df[['High', 'Low', 'Close']], columns=['High', 'Low', 'Close'])
    answer_df[['Low_period', 'High_period', 'RSV_period', 'K_period', 'D_period', 'J_period']] = 0

    # High[0], Low[1], Close[2], Low_period[3], High_period[4], RSV_period[5], K_period[6], D_period[7], J_period[8]
    answer_df.at[period - 1, 'K_period'] = 50
    answer_df.at[period - 1, 'D_period'] = 50
    answer_df.at[period - 1, 'J_period'] = 50
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np)):
        answer_np[x, 3] = min(answer_np[x - period + 1:x + 1, 1])
        answer_np[x, 4] = max(answer_np[x - period + 1:x + 1, 0])
        answer_np[x, 5] = (answer_np[x, 2] - answer_np[x, 3]) / (answer_np[x, 4] - answer_np[x, 3]) * 100

    for x in range(period, len(answer_np)):
        answer_np[x, 6] = (2 / 3) * answer_np[x - 1, 6] + (1 / 3) * answer_np[x, 5]
        answer_np[x, 7] = (2 / 3) * answer_np[x - 1, 7] + (1 / 3) * answer_np[x, 6]
        answer_np[x, 8] = (3 * answer_np[x, 6]) - (2 * answer_np[x, 7])

    answer_df = pd.DataFrame(answer_np, columns=[
        ['High', 'Low', 'Close', 'Low_period', 'High_period', 'RSV_period', 'K_period', 'D_period', 'J_period']])
    print(answer_df.to_string())
    return True


def obv():
    answer_df = pd.DataFrame(data_df[['Close', 'Volume']], columns=['Close', 'Volume'])
    answer_df['obv_indicator'] = 0

    # Close[0], Volume[1], obv_indicator[2]
    answer_pd = answer_df.to_numpy()
    for x in range(1, len(answer_pd)):
        if answer_pd[x, 0] > answer_pd[x - 1, 0]:
            answer_pd[x, 2] = answer_pd[x - 1, 2] + answer_pd[x, 1]
        elif answer_pd[x, 0] < answer_pd[x - 1, 0]:
            answer_pd[x, 2] = answer_pd[x - 1, 2] - answer_pd[x, 1]
        elif answer_pd[x, 0] == answer_pd[x - 1, 0]:
            answer_pd[x, 2] = answer_pd[x - 1, 2]

    return pd.DataFrame(answer_pd[:, 2], columns=['OBV'])


def cci(period):
    period = int(period)
    answer_df = simple_moving_average(period, 'typical_price')
    answer_df['mean_deviation'] = 0
    answer_df['cci'] = 0

    # typical_price[0], sma_of_typical_price[1], mean_deviation[2], cci[3]
    answer_np = answer_df.to_numpy()
    for x in range(period + period - 2, len(answer_np)):
        mean_deviation = np.full((period), answer_np[x, 1])
        answer_np[x, 2] = np.sum(np.abs(answer_np[x - period + 1:x + 1, 0] - mean_deviation)) / period
        answer_np[x, 3] = (answer_np[x, 0] - answer_np[x, 1]) / (0.015 * answer_np[x, 2])

    return pd.DataFrame(answer_np[:, 3], columns=['CCI_' + str(period)])


def stoch_rsi(length_rsi, length_stoch, smooth_k, smooth_d):
    length_rsi = int(length_rsi)
    length_stoch = int(length_stoch)
    smooth_k = int(smooth_k)
    smooth_d = int(smooth_d)
    answer_df = rsi(length_rsi)
    answer_df[['max_rsi', 'smooth_rsi', 'min_rsi', 'stoch_rsi', 'smooth_stoch_rsi']] = 0

    # rsi[0], smooth_rsi[1] max_rsi[2], min_rsi[3], stoch_rsi[4], smooth_stoch_rsi[5]
    answer_np = answer_df.to_numpy()

    for x in range(length_rsi + length_stoch - 1, len(answer_np)):
        answer_np[x][1] = np.mean(answer_np[x - smooth_k + 1:x + 1, 0])
        answer_np[x][2] = max(answer_np[x - length_stoch + 1: x + 1, 1])
        answer_np[x][3] = min(answer_np[x - length_stoch + 1: x + 1, 1])
        answer_np[x][4] = (answer_np[x][1] - answer_np[x][3]) / (answer_np[x][2] - answer_np[x][3])
        answer_np[x][5] = np.mean(answer_np[x - smooth_d + 1:x + 1, 4])

    return pd.DataFrame(answer_np[:,5], columns=['StochRSI_{}_{}_{}_{}'
                        .format(length_rsi, length_stoch, smooth_k, smooth_d)])


def wr(period):
    period = int(period)
    answer_df = pd.DataFrame(data_df[['High', 'Low', 'Close']], columns=['High', 'Low', 'Close'])
    answer_df[['highest_high', 'lowes_low', 'wr']] = 0

    # High[0], Low[1], Close[2], highest_high[3], lowes_low[4], wr[5]
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np)):
        answer_np[x, 3] = max(answer_np[x - period + 1:x + 1, 0])
        answer_np[x, 4] = min(answer_np[x - period + 1:x + 1, 1])
        answer_np[x, 5] = (answer_np[x, 3] - answer_np[x, 2]) - (answer_np[x, 3] - answer_np[x, 4])

    return pd.DataFrame(answer_np[:, 4], columns=['WR_' + str(period)])


# TODO
def dmi(period):
    period = int(period)
    return True


def mtm(period, source):
    period = int(period)
    answer_df = pd.DataFrame(data_df[[source]], columns=[source])
    answer_df[['mtm']] = 0

    # source[0], mtm[1]
    answer_np = answer_df.to_numpy()
    for x in range(period, len(answer_np)):
        answer_np[x][1] = answer_np[x][0] - answer_np[x - period][0]
    return pd.DataFrame(answer_np[:,1], columns=[f'MTM_{period}_{source}'])


def evm(period, divisor):
    period = int(period)
    divisor = int(divisor)
    answer_df = pd.DataFrame(data_df[['High', 'Low', 'Volume']])
    answer_df['distance_moved'] = 0
    answer_df['emv_1period'] = 0
    answer_df['sma_of_emv'] = 0

    # High[0], Close[1], Volume[2], distance_moved[3], emv_1period[4], sma_of_emv[5]
    answer_np = answer_df.to_numpy()
    for x in range(1, len(answer_np)):
        answer_np[x, 3] = ((answer_np[x, 0] + answer_np[x, 1]) / 2) - ((answer_np[x-1, 0] + answer_np[x-1, 1]) / 2)
        answer_np[x, 4] = answer_np[x, 3] / ((answer_np[x, 2] / divisor) / (answer_np[x, 0] - answer_np[x, 1]))

    for y in range(period, len(answer_np)):
        answer_np[y][5] = np.mean(answer_np[y - period + 1:y + 1, 4])

    return pd.DataFrame(answer_np[:,5], columns=['EMV_{}_{}'.format(period, divisor)])

indicator_function_name = {
    'SMA': simple_moving_average,
    'EMA': exponential_moving_average,
    'WMA': weighted_moving_average,
    'BOLL - Upper Band': bollinger_band_upper,
    'BOLL - Lower Band': bollinger_band_lower,
    'VWAP': volume_weighted_average_price,
    'TRIX': trix,
    'SAR': sar,
    'MACD - MACD Line': macd_line,
    'MACD - Singal Line': macd_signal_line,
    'RSI': rsi,
    'KDJ': kdj,
    'OBV': obv,
    'CCI': cci,
    'StochRSI': stoch_rsi,
    'WR': wr,
    'DMI': dmi,
    'MTM': mtm,
    'EMV': evm,
    'Value': None,
    'Open': None,
    'High': None,
    'Low': None,
    'Close': None,
    'Volume': None
}