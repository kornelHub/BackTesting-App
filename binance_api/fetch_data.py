from utilities.helpers import date_to_milliseconds
from utilities import helpers
import pandas as pd
import os
from stat import S_IREAD
import requests


def download_data_to_file(start_time, end_time, interval, currency_pair_symbol, path_to_file):
    url = 'https://api.binance.com/api/v3/klines'
    params = {
        'symbol': currency_pair_symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit': 1000
    }
    candles = requests.get(url, params=params)
    candles_df = pd.DataFrame(candles.json(), columns=helpers.colums_name_from_binance)
    candles_df = candles_df.round(decimals=5)
    if len(candles_df) > 1:
        close_time = candles_df['CloseTime'].iloc[-1]
    else:
        close_time = 0
    candles_df = candles_df.drop(
        columns=['QuoteAssetVolume', 'NumberOfTrades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ingore'])
    candles_df.dropna()

    if candles_df.iloc[-1]['CloseTime'] > date_to_milliseconds("now UTC") + 10000:
        candles_df = candles_df[:-1]

    if not os.path.exists(path_to_file):
        file = open(path_to_file, "w")
        file.write(currency_pair_symbol + '\n')
        file.close()
        candles_df.to_csv(path_to_file, sep=';', index=False, mode='a', header=True)
    else:
        candles_df.to_csv(path_to_file, sep=';', index=False, mode='a', header=False)
    return close_time

def create_data_from_binance(start_time, end_time, interval, currency_pair_symbol, path_to_file):
    close_time_of_last_value_in_file = download_data_to_file(start_time=start_time,
                                                             end_time=end_time,
                                                             interval=interval,
                                                             currency_pair_symbol=currency_pair_symbol,
                                                             path_to_file=path_to_file)
    if close_time_of_last_value_in_file + 1 < end_time:
        create_data_from_binance(start_time=close_time_of_last_value_in_file + 1,
                                 end_time=end_time,
                                 interval=interval,
                                 currency_pair_symbol=currency_pair_symbol,
                                 path_to_file=path_to_file)


def create_csv_with_ohlcv_data(start_time, end_time, interval, currency_pair_symbol, path_to_file):
    create_data_from_binance(start_time=start_time,
                             end_time=end_time,
                             interval=interval,
                             currency_pair_symbol=currency_pair_symbol,
                             path_to_file=path_to_file)
    os.chmod(path_to_file, S_IREAD) # add read_only attribute to created file


def delete_data(file_name):
    file = open(file_name, mode="r+")
    file.truncate(0)
    file.close()
    print('****DataErased****')