import pandas as pd
import numpy as np

data_df = pd.read_csv("data/data.csv", sep=';')


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
        answer_df = pd.DataFrame(answer_np, columns=[['typical_price', 'sma_of_typical_price']])
        return answer_df
    else:
        answer_df = pd.DataFrame(answer_np[:, 1], columns=['SMA_' + str(period) + '_' + source])
        return answer_df


def exponential_moving_average(period, source):
    period = int(period)
    ema_multiplier = 2 / (period + 1)
    answer_df = data_df[source].copy()
    answer_np = answer_df.to_numpy()
    answer_np = answer_np[:, np.newaxis]
    answer_np = np.concatenate((answer_np, np.zeros((len(answer_np), 1))), axis=1)
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
    answer_df = pd.DataFrame(answer_np[:, 1], columns=['EMA_' + str(period) + '_' + source])
    return answer_df


def exponential_moving_average_helper(data_df, period, source):
    ema_multiplier = 2 / (period + 1)
    answer_df = data_df[source].copy()
    answer_np = answer_df.to_numpy()
    answer_np = answer_np[:, np.newaxis]
    answer_np = np.concatenate((answer_np, np.zeros((len(answer_np), 1))), axis=1)
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
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np - 1)):
        weighted_sum, divider = 0, 0
        for y in range(1, period + 1):
            weighted_sum += answer_np[x + 1 - y, 0] * (period + 1 - y)
            divider += y
        answer_np[x][1] = weighted_sum / divider
    answer_df = pd.DataFrame(answer_np[:, 1], columns=['WMA_' + str(period) + '_' + source])
    return answer_df


def bollinger_band_upper(period, multiplier):
    period = int(period)
    multiplier = int(multiplier)
    # High_Low_Close_SMA, High_Low_Close_SMA_period_SMA
    answer_df = simple_moving_average(period, 'typical_price')
    answer_df['standard_deviation'] = 0
    answer_df['bollinger_band_upper'] = 0
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np)):
        # standard_deviation assign
        answer_np[x, 1] = np.std(answer_np[x + 1 - period:x + 1, 0], axis=0, dtype=np.float64)
        # bollinger_band_upper assign
        answer_np[x, 2] = answer_np[x, 1] + (answer_np[x, 2] * multiplier)

    answer_df = pd.DataFrame(answer_np[:, 2], columns=['BOLL_Upper_' + str(period) + '_' + str(multiplier)])
    # print(answer_df.to_string())
    return answer_df


def bollinger_band_lower(period, multiplier):
    period = int(period)
    multiplier = int(multiplier)
    # High_Low_Close_SMA, High_Low_Close_SMA_period_SMA
    answer_df = simple_moving_average(period, 'typical_price')
    answer_df['standard_deviation'] = 0
    answer_df['bollinger_band_lower'] = 0
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np)):
        # standard_deviation assign
        answer_np[x, 1] = np.std(answer_np[x + 1 - period:x + 1, 0], axis=0, dtype=np.float64)
        # bollinger_band_upper assign
        answer_np[x, 2] = answer_np[x, 1] - (answer_np[x, 2] * multiplier)

    answer_df = pd.DataFrame(answer_np[:, 2], columns=['BOLL_Lower_' + str(period) + '_' + str(multiplier)])
    # print(answer_df.to_string())
    return answer_df


# TODO: do zastanowienia czy potrzeba
def volume_weighted_average_price():
    return True


def trix(period):
    answer_df = pd.DataFrame(exponential_moving_average_helper(data_df, period, 'Close'), columns=['Open', '1st_ema'])
    answer_df[['2nd_ema', '3rd_ema']] = 0
    answer_df['2nd_ema'] = exponential_moving_average_helper(answer_df, period, '1st_ema')[:, 1]
    answer_df['3rd_ema'] = exponential_moving_average_helper(answer_df, period, '2nd_ema')[:, 1]
    answer_df['trix'] = 0
    answer_np = answer_df[['3rd_ema', 'trix']].to_numpy()
    for x in range((period * 3) - 2, len(answer_np)):
        answer_np[x, 1] = (answer_np[x, 0] - answer_np[x - 1, 0]) / answer_np[x - 1, 0]
    answer_df = pd.DataFrame(answer_np[:, 1], columns=['TRIX_' + str(period)])
    return answer_df


# TODO: trudne do zrobienie, ogarne jak bede mial czas :)
def sar(period, source):
    return True


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
        columns={'MACD': 'MACD_Line_' + str(period_1) + '_' + str(period_2) + '_' + str(period_3) + '_' + source})
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
        columns={'third_period_ema_of_MACD': 'MACD_Signal_Line_' + str(period_1) + '_' + str(period_2) + '_' + str(period_3) + '_' + source})
    # print(answer_df.to_string())
    return answer_df.iloc[:, 4]


def rsi(period):
    period = int(period)
    answer_df = pd.DataFrame(data_df['Close'], columns=['Close'])
    answer_df[['close_price_change', 'average_gain', 'average_loss', 'rsi']] = 0
    # Close, close_price_change, average_gain, average_loss, rsi
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
    # print(answer_df.to_string())
    return answer_df


def kdj(period, k_smooth, d_smooth):
    period = int(period)
    k_smooth = int(k_smooth)
    d_smooth = int(d_smooth)
    answer_df = pd.DataFrame(data_df[['High', 'Low', 'Close']], columns=['High', 'Low', 'Close'])
    answer_df[['Low_period', 'High_period', 'RSV_period', 'K_period', 'D_period', 'J_period']] = 0
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
    answer_pd = answer_df.to_numpy()
    for x in range(1, len(answer_pd)):
        if answer_pd[x, 0] > answer_pd[x - 1, 0]:
            answer_pd[x, 2] = answer_pd[x - 1, 2] + answer_pd[x, 1]
        elif answer_pd[x, 0] < answer_pd[x - 1, 0]:
            answer_pd[x, 2] = answer_pd[x - 1, 2] - answer_pd[x, 1]
        elif answer_pd[x, 0] == answer_pd[x - 1, 0]:
            answer_pd[x, 2] = answer_pd[x - 1, 2]

    answer_df = pd.DataFrame(answer_pd[:, 2], columns=['OBV'])
    # print(answer_df.to_string())
    return answer_df


def cci(period):
    period = int(period)
    answer_df = simple_moving_average(period, 'typical_price')
    answer_df['mean_deviation'] = 0
    answer_df['cci'] = 0

    answer_np = answer_df.to_numpy()
    for x in range(period + period - 2, len(answer_np)):
        mean_deviation = np.full((period), answer_np[x, 1])
        answer_np[x, 2] = np.sum(np.abs(answer_np[x - period + 1:x + 1, 0] - mean_deviation)) / period
        answer_np[x, 3] = (answer_np[x, 0] - answer_np[x, 1]) / (0.015 * answer_np[x, 2])

    answer_df = pd.DataFrame(answer_np[:, 3], columns=['CCI_' + str(period)])
    # print(answer_df.to_string())
    return answer_df


def stoch_rsi():
    return True


def wr(period):
    period = int(period)
    answer_df = pd.DataFrame(data_df[['High', 'Low', 'Close']], columns=['High', 'Low', 'Close'])
    answer_df[['highest_high', 'lowes_low', 'wr']] = 0
    answer_np = answer_df.to_numpy()
    for x in range(period - 1, len(answer_np)):
        answer_np[x, 3] = max(answer_np[x - period + 1:x + 1, 0])
        answer_np[x, 4] = min(answer_np[x - period + 1:x + 1, 1])
        answer_np[x, 5] = (answer_np[x, 3] - answer_np[x, 2]) - (answer_np[x, 3] - answer_np[x, 4])

    answer_df = pd.DataFrame(answer_np[:, 4], columns=['WR_' + str(period)])
    # print(answer_df.to_string())
    return answer_df


def dmi(period):
    period = int(period)
    return True


def mtm():
    return True


def evm(period, divisor):
    period = int(period)
    divisor = int(divisor)
    answer_df = pd.DataFrame(data_df[['High', 'Low', 'Volume']])
    answer_df['distance_moved'] = 0
    answer_df['emv_1period'] = 0
    answer_df['sma_of_emv'] = 0
    answer_np = answer_df.to_numpy()
    for x in range(1, len(answer_np)):
        answer_np[x, 3] = ((answer_np[x, 0] + answer_np[x, 1]) / 2) - ((answer_np[x-1, 0] + answer_np[x-1, 1]) / 2)
        answer_np[x, 4] = answer_np[x, 3] / ((answer_np[x, 2] / divisor) / (answer_np[x, 0] - answer_np[x, 1]))

    for y in range(period, len(answer_np)):
        answer_np[y][5] = np.mean(answer_np[y - period + 1:y + 1, 4])

    answer_df = pd.DataFrame(answer_np[:,5], columns=['EVM_'+str(period)+'_'+str(divisor)])
    print(answer_df.to_string())
    return answer_df
