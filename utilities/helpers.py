import datetime as dt
import pytz
import pandas as pd
from PySide2.QtWidgets import QLineEdit, QComboBox, QPushButton, QPlainTextEdit, QTreeWidget
from datetime import datetime
from typing import Union, Optional, Dict
import dateparser
import os
from stat import S_IREAD

path_to_csv_file = ''
colums_name_from_binance = ['Opentime', 'Open', 'High', 'Low', 'Close', 'Volume', 'CloseTime', 'QuoteAssetVolume',
                            'NumberOfTrades', 'TakerBuyBaseAssetVolume', 'TakerBuyQuoteAssetVolume', 'Ingore']
columns_name_string = 'Opentime;Open;High;Low;Close;Volume;CloseTime'


def load_ohlcv_data_from_csv_file():
    return pd.read_csv(path_to_csv_file, sep=';', skiprows=[0])


def hide_error_message(error_message_label):
    error_message_label.hide()


def show_error_message(error_message_label, message_text):
    error_message_label.show()
    error_message_label.setText(message_text)


def check_if_all_fields_have_text(list_of_fields):
    is_field_has_text = []
    for field in list_of_fields:
        if isinstance(field, QLineEdit) or isinstance(field, QPushButton):
            if field.text():
                is_field_has_text.append(True)
                field.setProperty('invalid', False)
                field.style().polish(field)
            else:
                is_field_has_text.append(False)
                field.setProperty('invalid', True)
                field.style().polish(field)
        elif isinstance(field, QComboBox):
            if field.currentText():
                is_field_has_text.append(True)
                field.setProperty('invalid', False)
                field.style().polish(field)
            else:
                is_field_has_text.append(False)
                field.setProperty('invalid', True)
                field.style().polish(field)
        elif isinstance(field, QPlainTextEdit):
            if field.toPlainText():
                is_field_has_text.append(True)
                field.setProperty('invalid', False)
                field.style().polish(field)
            else:
                is_field_has_text.append(False)
                field.setProperty('invalid', True)
                field.style().polish(field)
        elif isinstance(field, QTreeWidget):
            if field.topLevelItem(0):
                is_field_has_text.append(True)
                field.setProperty('invalid', False)
                field.style().polish(field)
            else:
                is_field_has_text.append(False)
                field.setProperty('invalid', True)
                field.style().polish(field)

    return is_field_has_text


def apply_read_only_attribute_to_file(path_to_file):
    os.chmod(path_to_file, S_IREAD)


def return_index_of_first_non_zero_row(data_df):
    data_np = data_df.to_numpy()
    for x in range(len(data_np)):
        if 0 not in data_np[x][7:]:
            return x


def convert_milliseconds_to_date(time_in_utc_miloseconds):
    converted_date = dt.datetime.fromtimestamp(time_in_utc_miloseconds / 1000.0, tz=pytz.utc)
    return converted_date

def date_to_milliseconds(date_str: str) -> int:
    """Convert UTC date to milliseconds

    If using offset strings add "UTC" to date string e.g. "now UTC", "11 hours ago UTC"

    See dateparse docs for formats http://dateparser.readthedocs.io/en/latest/

    :param date_str: date in readable format, i.e. "January 01, 2018", "11 hours ago UTC", "now UTC"
    """
    # get epoch value in UTC
    epoch: datetime = datetime.utcfromtimestamp(0).replace(tzinfo=pytz.utc)
    # parse our date string
    d: Optional[datetime] = dateparser.parse(date_str)
    # if the date is not timezone aware apply UTC timezone
    if d.tzinfo is None or d.tzinfo.utcoffset(d) is None:
        d = d.replace(tzinfo=pytz.utc)

    # return the difference in time
    return int((d - epoch).total_seconds() * 1000.0)


def create_cryptocurrency_dictionary():
    # get all_margin_dict from binance_api via Postman
    # Binance spot API > Margin > Isolated > Get All Isolated Margin Pairs(MARKET_DATA)
    # Response:
    # [
    #     {
    #         "symbol": "1INCHBTC",
    #         "base": "1INCH",
    #         "quote": "BTC",
    #         "isMarginTrade": true,
    #         "isBuyAllowed": true,
    #         "isSellAllowed": true
    #     },
    #     {
    #         "symbol": "1INCHUSDT",
    #         "base": "1INCH",
    #         "quote": "USDT",
    #         "isMarginTrade": true,
    #         "isBuyAllowed": true,
    #         "isSellAllowed": true
    #     }
    # ]
    all_margin_dict = []
    dictionary = {}
    for x in all_margin_dict:
        dictionary[x['symbol']] = {
            "base": x['base'],
            "quote": x['quote']
        }
    print(dictionary)  # paste output into cryptocurrency_pair_dict


# add_strategy_button_style_sheet_normal = "QPushButton {\ncolor: rgb(255, 255, 255);\nbackground-color: rgb(70,70,70);\nborder: 0px sold;\nborder-radius: 10px;\n\n}\nQPushButton:hover {\n	 border: 2px solid rgb(85,85,85);\n}"
# add_strategy_button_style_sheet_clicked = "QPushButton {\ncolor: rgb(255, 255, 255);\nbackground-color: rgb(85, 170, 255);\nborder: 0px sold;\nborder-radius: 10px;\n\n}"

time_difference_dictionary = {
    '1m': 60000,
    '3m': 180000,
    '5m': 300000,
    '15m': 900000,
    '30m': 1800000,
    '1H': 3600000,
    '2H': 7200000,
    '4H': 14400000,
    '8H': 28800000,
    '12H': 43200000,
    '1D': 86400000,
    '3D': 259200000,
    '1W': 604800000
}

cryptocurrency_pair_dict = {'1INCHBTC': {'base': '1INCH', 'quote': 'BTC'},
                            '1INCHUSDT': {'base': '1INCH', 'quote': 'USDT'},
                            'AAVEBTC': {'base': 'AAVE', 'quote': 'BTC'}, 'AAVEBUSD': {'base': 'AAVE', 'quote': 'BUSD'},
                            'AAVEUSDT': {'base': 'AAVE', 'quote': 'USDT'}, 'ADABTC': {'base': 'ADA', 'quote': 'BTC'},
                            'ADABUSD': {'base': 'ADA', 'quote': 'BUSD'}, 'ADAETH': {'base': 'ADA', 'quote': 'ETH'},
                            'ADAEUR': {'base': 'ADA', 'quote': 'EUR'}, 'ADAUSDT': {'base': 'ADA', 'quote': 'USDT'},
                            'AKROBTC': {'base': 'AKRO', 'quote': 'BTC'}, 'AKROUSDT': {'base': 'AKRO', 'quote': 'USDT'},
                            'ALGOBTC': {'base': 'ALGO', 'quote': 'BTC'}, 'ALGOBUSD': {'base': 'ALGO', 'quote': 'BUSD'},
                            'ALGOUSDT': {'base': 'ALGO', 'quote': 'USDT'},
                            'ALPHABTC': {'base': 'ALPHA', 'quote': 'BTC'},
                            'ALPHABUSD': {'base': 'ALPHA', 'quote': 'BUSD'},
                            'ALPHAUSDT': {'base': 'ALPHA', 'quote': 'USDT'},
                            'ANKRBTC': {'base': 'ANKR', 'quote': 'BTC'}, 'ANKRUSDT': {'base': 'ANKR', 'quote': 'USDT'},
                            'ANTBTC': {'base': 'ANT', 'quote': 'BTC'}, 'ANTBUSD': {'base': 'ANT', 'quote': 'BUSD'},
                            'ANTUSDT': {'base': 'ANT', 'quote': 'USDT'}, 'ARDRBTC': {'base': 'ARDR', 'quote': 'BTC'},
                            'ARDRUSDT': {'base': 'ARDR', 'quote': 'USDT'}, 'ARPABTC': {'base': 'ARPA', 'quote': 'BTC'},
                            'ARPAUSDT': {'base': 'ARPA', 'quote': 'USDT'}, 'ATOMBTC': {'base': 'ATOM', 'quote': 'BTC'},
                            'ATOMBUSD': {'base': 'ATOM', 'quote': 'BUSD'},
                            'ATOMUSDT': {'base': 'ATOM', 'quote': 'USDT'}, 'AUDUSDT': {'base': 'AUD', 'quote': 'USDT'},
                            'AVABTC': {'base': 'AVA', 'quote': 'BTC'}, 'AVABUSD': {'base': 'AVA', 'quote': 'BUSD'},
                            'AVAXBTC': {'base': 'AVAX', 'quote': 'BTC'}, 'AVAXBUSD': {'base': 'AVAX', 'quote': 'BUSD'},
                            'AVAXUSDT': {'base': 'AVAX', 'quote': 'USDT'}, 'AXSBTC': {'base': 'AXS', 'quote': 'BTC'},
                            'AXSBUSD': {'base': 'AXS', 'quote': 'BUSD'}, 'AXSUSDT': {'base': 'AXS', 'quote': 'USDT'},
                            'BALBTC': {'base': 'BAL', 'quote': 'BTC'}, 'BALBUSD': {'base': 'BAL', 'quote': 'BUSD'},
                            'BALUSDT': {'base': 'BAL', 'quote': 'USDT'}, 'BANDBTC': {'base': 'BAND', 'quote': 'BTC'},
                            'BANDUSDT': {'base': 'BAND', 'quote': 'USDT'}, 'BATBTC': {'base': 'BAT', 'quote': 'BTC'},
                            'BATBUSD': {'base': 'BAT', 'quote': 'BUSD'}, 'BATUSDT': {'base': 'BAT', 'quote': 'USDT'},
                            'BCHBTC': {'base': 'BCH', 'quote': 'BTC'}, 'BCHBUSD': {'base': 'BCH', 'quote': 'BUSD'},
                            'BCHEUR': {'base': 'BCH', 'quote': 'EUR'}, 'BCHUSDT': {'base': 'BCH', 'quote': 'USDT'},
                            'BELBTC': {'base': 'BEL', 'quote': 'BTC'}, 'BELBUSD': {'base': 'BEL', 'quote': 'BUSD'},
                            'BELUSDT': {'base': 'BEL', 'quote': 'USDT'}, 'BLZBTC': {'base': 'BLZ', 'quote': 'BTC'},
                            'BLZBUSD': {'base': 'BLZ', 'quote': 'BUSD'}, 'BLZUSDT': {'base': 'BLZ', 'quote': 'USDT'},
                            'BNBBTC': {'base': 'BNB', 'quote': 'BTC'}, 'BNBBUSD': {'base': 'BNB', 'quote': 'BUSD'},
                            'BNBETH': {'base': 'BNB', 'quote': 'ETH'}, 'BNBEUR': {'base': 'BNB', 'quote': 'EUR'},
                            'BNBGBP': {'base': 'BNB', 'quote': 'GBP'}, 'BNBUSDT': {'base': 'BNB', 'quote': 'USDT'},
                            'BNTBTC': {'base': 'BNT', 'quote': 'BTC'}, 'BNTBUSD': {'base': 'BNT', 'quote': 'BUSD'},
                            'BNTUSDT': {'base': 'BNT', 'quote': 'USDT'}, 'BTCAUD': {'base': 'BTC', 'quote': 'AUD'},
                            'BTCBUSD': {'base': 'BTC', 'quote': 'BUSD'}, 'BTCEUR': {'base': 'BTC', 'quote': 'EUR'},
                            'BTCGBP': {'base': 'BTC', 'quote': 'GBP'}, 'BTCSTBTC': {'base': 'BTCST', 'quote': 'BTC'},
                            'BTCSTUSDT': {'base': 'BTCST', 'quote': 'USDT'},
                            'BTCUSDT': {'base': 'BTC', 'quote': 'USDT'}, 'BTSBTC': {'base': 'BTS', 'quote': 'BTC'},
                            'BTSUSDT': {'base': 'BTS', 'quote': 'USDT'}, 'BTTBUSD': {'base': 'BTT', 'quote': 'BUSD'},
                            'BTTUSDT': {'base': 'BTT', 'quote': 'USDT'}, 'BUSDUSDT': {'base': 'BUSD', 'quote': 'USDT'},
                            'BZRXBTC': {'base': 'BZRX', 'quote': 'BTC'}, 'BZRXBUSD': {'base': 'BZRX', 'quote': 'BUSD'},
                            'BZRXUSDT': {'base': 'BZRX', 'quote': 'USDT'},
                            'CAKEBUSD': {'base': 'CAKE', 'quote': 'BUSD'}, 'CELOBTC': {'base': 'CELO', 'quote': 'BTC'},
                            'CELOUSDT': {'base': 'CELO', 'quote': 'USDT'}, 'CELRBTC': {'base': 'CELR', 'quote': 'BTC'},
                            'CELRUSDT': {'base': 'CELR', 'quote': 'USDT'}, 'CHRBTC': {'base': 'CHR', 'quote': 'BTC'},
                            'CHRUSDT': {'base': 'CHR', 'quote': 'USDT'}, 'CHZBTC': {'base': 'CHZ', 'quote': 'BTC'},
                            'CHZUSDT': {'base': 'CHZ', 'quote': 'USDT'}, 'COMPBTC': {'base': 'COMP', 'quote': 'BTC'},
                            'COMPBUSD': {'base': 'COMP', 'quote': 'BUSD'},
                            'COMPUSDT': {'base': 'COMP', 'quote': 'USDT'}, 'COTIBTC': {'base': 'COTI', 'quote': 'BTC'},
                            'COTIUSDT': {'base': 'COTI', 'quote': 'USDT'}, 'CRVBTC': {'base': 'CRV', 'quote': 'BTC'},
                            'CRVBUSD': {'base': 'CRV', 'quote': 'BUSD'}, 'CRVUSDT': {'base': 'CRV', 'quote': 'USDT'},
                            'CTKBTC': {'base': 'CTK', 'quote': 'BTC'}, 'CTKBUSD': {'base': 'CTK', 'quote': 'BUSD'},
                            'CTKUSDT': {'base': 'CTK', 'quote': 'USDT'}, 'CTSIBTC': {'base': 'CTSI', 'quote': 'BTC'},
                            'CTSIBUSD': {'base': 'CTSI', 'quote': 'BUSD'},
                            'CTSIUSDT': {'base': 'CTSI', 'quote': 'USDT'}, 'CVCBTC': {'base': 'CVC', 'quote': 'BTC'},
                            'CVCUSDT': {'base': 'CVC', 'quote': 'USDT'}, 'DASHBTC': {'base': 'DASH', 'quote': 'BTC'},
                            'DASHBUSD': {'base': 'DASH', 'quote': 'BUSD'},
                            'DASHUSDT': {'base': 'DASH', 'quote': 'USDT'}, 'DATABTC': {'base': 'DATA', 'quote': 'BTC'},
                            'DATABUSD': {'base': 'DATA', 'quote': 'BUSD'},
                            'DATAUSDT': {'base': 'DATA', 'quote': 'USDT'}, 'DCRBTC': {'base': 'DCR', 'quote': 'BTC'},
                            'DCRUSDT': {'base': 'DCR', 'quote': 'USDT'}, 'DGBBTC': {'base': 'DGB', 'quote': 'BTC'},
                            'DGBBUSD': {'base': 'DGB', 'quote': 'BUSD'}, 'DGBUSDT': {'base': 'DGB', 'quote': 'USDT'},
                            'DIABTC': {'base': 'DIA', 'quote': 'BTC'}, 'DIABUSD': {'base': 'DIA', 'quote': 'BUSD'},
                            'DIAUSDT': {'base': 'DIA', 'quote': 'USDT'}, 'DNTBTC': {'base': 'DNT', 'quote': 'BTC'},
                            'DNTBUSD': {'base': 'DNT', 'quote': 'BUSD'}, 'DNTUSDT': {'base': 'DNT', 'quote': 'USDT'},
                            'DOCKBTC': {'base': 'DOCK', 'quote': 'BTC'}, 'DOCKUSDT': {'base': 'DOCK', 'quote': 'USDT'},
                            'DOGEBTC': {'base': 'DOGE', 'quote': 'BTC'}, 'DOGEBUSD': {'base': 'DOGE', 'quote': 'BUSD'},
                            'DOGEUSDT': {'base': 'DOGE', 'quote': 'USDT'}, 'DOTBTC': {'base': 'DOT', 'quote': 'BTC'},
                            'DOTBUSD': {'base': 'DOT', 'quote': 'BUSD'}, 'DOTEUR': {'base': 'DOT', 'quote': 'EUR'},
                            'DOTUSDT': {'base': 'DOT', 'quote': 'USDT'}, 'DUSKBTC': {'base': 'DUSK', 'quote': 'BTC'},
                            'DUSKUSDT': {'base': 'DUSK', 'quote': 'USDT'}, 'EGLDBTC': {'base': 'EGLD', 'quote': 'BTC'},
                            'EGLDBUSD': {'base': 'EGLD', 'quote': 'BUSD'},
                            'EGLDUSDT': {'base': 'EGLD', 'quote': 'USDT'}, 'ENJBTC': {'base': 'ENJ', 'quote': 'BTC'},
                            'ENJBUSD': {'base': 'ENJ', 'quote': 'BUSD'}, 'ENJUSDT': {'base': 'ENJ', 'quote': 'USDT'},
                            'EOSBTC': {'base': 'EOS', 'quote': 'BTC'}, 'EOSBUSD': {'base': 'EOS', 'quote': 'BUSD'},
                            'EOSUSDT': {'base': 'EOS', 'quote': 'USDT'}, 'ETCBTC': {'base': 'ETC', 'quote': 'BTC'},
                            'ETCBUSD': {'base': 'ETC', 'quote': 'BUSD'}, 'ETCUSDT': {'base': 'ETC', 'quote': 'USDT'},
                            'ETHBTC': {'base': 'ETH', 'quote': 'BTC'}, 'ETHBUSD': {'base': 'ETH', 'quote': 'BUSD'},
                            'ETHEUR': {'base': 'ETH', 'quote': 'EUR'}, 'ETHGBP': {'base': 'ETH', 'quote': 'GBP'},
                            'ETHUSDT': {'base': 'ETH', 'quote': 'USDT'}, 'EURBUSD': {'base': 'EUR', 'quote': 'BUSD'},
                            'EURUSDT': {'base': 'EUR', 'quote': 'USDT'}, 'FETBTC': {'base': 'FET', 'quote': 'BTC'},
                            'FETUSDT': {'base': 'FET', 'quote': 'USDT'}, 'FILBTC': {'base': 'FIL', 'quote': 'BTC'},
                            'FILBUSD': {'base': 'FIL', 'quote': 'BUSD'}, 'FILUSDT': {'base': 'FIL', 'quote': 'USDT'},
                            'FLMBTC': {'base': 'FLM', 'quote': 'BTC'}, 'FLMBUSD': {'base': 'FLM', 'quote': 'BUSD'},
                            'FLMUSDT': {'base': 'FLM', 'quote': 'USDT'},
                            'FRONTBUSD': {'base': 'FRONT', 'quote': 'BUSD'}, 'FTMBTC': {'base': 'FTM', 'quote': 'BTC'},
                            'FTMUSDT': {'base': 'FTM', 'quote': 'USDT'}, 'FTTBTC': {'base': 'FTT', 'quote': 'BTC'},
                            'FTTUSDT': {'base': 'FTT', 'quote': 'USDT'}, 'FUNBTC': {'base': 'FUN', 'quote': 'BTC'},
                            'FUNUSDT': {'base': 'FUN', 'quote': 'USDT'}, 'GBPBUSD': {'base': 'GBP', 'quote': 'BUSD'},
                            'GBPUSDT': {'base': 'GBP', 'quote': 'USDT'}, 'GRTBTC': {'base': 'GRT', 'quote': 'BTC'},
                            'GRTETH': {'base': 'GRT', 'quote': 'ETH'}, 'GRTUSDT': {'base': 'GRT', 'quote': 'USDT'},
                            'GTOBTC': {'base': 'GTO', 'quote': 'BTC'}, 'GTOUSDT': {'base': 'GTO', 'quote': 'USDT'},
                            'GXSBTC': {'base': 'GXS', 'quote': 'BTC'}, 'GXSUSDT': {'base': 'GXS', 'quote': 'USDT'},
                            'HARDBTC': {'base': 'HARD', 'quote': 'BTC'}, 'HARDUSDT': {'base': 'HARD', 'quote': 'USDT'},
                            'HBARBTC': {'base': 'HBAR', 'quote': 'BTC'}, 'HBARBUSD': {'base': 'HBAR', 'quote': 'BUSD'},
                            'HBARUSDT': {'base': 'HBAR', 'quote': 'USDT'}, 'HIVEBTC': {'base': 'HIVE', 'quote': 'BTC'},
                            'HIVEUSDT': {'base': 'HIVE', 'quote': 'USDT'}, 'ICXBTC': {'base': 'ICX', 'quote': 'BTC'},
                            'ICXBUSD': {'base': 'ICX', 'quote': 'BUSD'}, 'ICXUSDT': {'base': 'ICX', 'quote': 'USDT'},
                            'INJBTC': {'base': 'INJ', 'quote': 'BTC'}, 'INJBUSD': {'base': 'INJ', 'quote': 'BUSD'},
                            'INJUSDT': {'base': 'INJ', 'quote': 'USDT'}, 'IOSTBTC': {'base': 'IOST', 'quote': 'BTC'},
                            'IOSTUSDT': {'base': 'IOST', 'quote': 'USDT'}, 'IOTABTC': {'base': 'IOTA', 'quote': 'BTC'},
                            'IOTABUSD': {'base': 'IOTA', 'quote': 'BUSD'},
                            'IOTAUSDT': {'base': 'IOTA', 'quote': 'USDT'}, 'IOTXBTC': {'base': 'IOTX', 'quote': 'BTC'},
                            'IOTXUSDT': {'base': 'IOTX', 'quote': 'USDT'}, 'IRISBTC': {'base': 'IRIS', 'quote': 'BTC'},
                            'IRISBUSD': {'base': 'IRIS', 'quote': 'BUSD'},
                            'IRISUSDT': {'base': 'IRIS', 'quote': 'USDT'}, 'JSTBTC': {'base': 'JST', 'quote': 'BTC'},
                            'JSTBUSD': {'base': 'JST', 'quote': 'BUSD'}, 'JSTUSDT': {'base': 'JST', 'quote': 'USDT'},
                            'KAVABTC': {'base': 'KAVA', 'quote': 'BTC'}, 'KAVAUSDT': {'base': 'KAVA', 'quote': 'USDT'},
                            'KMDBTC': {'base': 'KMD', 'quote': 'BTC'}, 'KMDBUSD': {'base': 'KMD', 'quote': 'BUSD'},
                            'KMDUSDT': {'base': 'KMD', 'quote': 'USDT'}, 'KNCBTC': {'base': 'KNC', 'quote': 'BTC'},
                            'KNCBUSD': {'base': 'KNC', 'quote': 'BUSD'}, 'KNCUSDT': {'base': 'KNC', 'quote': 'USDT'},
                            'KSMBTC': {'base': 'KSM', 'quote': 'BTC'}, 'KSMBUSD': {'base': 'KSM', 'quote': 'BUSD'},
                            'KSMUSDT': {'base': 'KSM', 'quote': 'USDT'}, 'LENDBTC': {'base': 'LEND', 'quote': 'BTC'},
                            'LENDUSDT': {'base': 'LEND', 'quote': 'USDT'}, 'LINKBTC': {'base': 'LINK', 'quote': 'BTC'},
                            'LINKBUSD': {'base': 'LINK', 'quote': 'BUSD'}, 'LINKEUR': {'base': 'LINK', 'quote': 'EUR'},
                            'LINKUSDT': {'base': 'LINK', 'quote': 'USDT'}, 'LITBTC': {'base': 'LIT', 'quote': 'BTC'},
                            'LITUSDT': {'base': 'LIT', 'quote': 'USDT'}, 'LOOMBTC': {'base': 'LOOM', 'quote': 'BTC'},
                            'LRCBTC': {'base': 'LRC', 'quote': 'BTC'}, 'LRCBUSD': {'base': 'LRC', 'quote': 'BUSD'},
                            'LRCUSDT': {'base': 'LRC', 'quote': 'USDT'}, 'LSKBTC': {'base': 'LSK', 'quote': 'BTC'},
                            'LSKUSDT': {'base': 'LSK', 'quote': 'USDT'}, 'LTCBTC': {'base': 'LTC', 'quote': 'BTC'},
                            'LTCBUSD': {'base': 'LTC', 'quote': 'BUSD'}, 'LTCEUR': {'base': 'LTC', 'quote': 'EUR'},
                            'LTCUSDT': {'base': 'LTC', 'quote': 'USDT'}, 'LTOBTC': {'base': 'LTO', 'quote': 'BTC'},
                            'LTOUSDT': {'base': 'LTO', 'quote': 'USDT'}, 'LUNABTC': {'base': 'LUNA', 'quote': 'BTC'},
                            'LUNABUSD': {'base': 'LUNA', 'quote': 'BUSD'},
                            'LUNAUSDT': {'base': 'LUNA', 'quote': 'USDT'}, 'MANABTC': {'base': 'MANA', 'quote': 'BTC'},
                            'MANABUSD': {'base': 'MANA', 'quote': 'BUSD'},
                            'MANAUSDT': {'base': 'MANA', 'quote': 'USDT'},
                            'MATICBTC': {'base': 'MATIC', 'quote': 'BTC'},
                            'MATICBUSD': {'base': 'MATIC', 'quote': 'BUSD'},
                            'MATICUSDT': {'base': 'MATIC', 'quote': 'USDT'}, 'MDTBTC': {'base': 'MDT', 'quote': 'BTC'},
                            'MDTUSDT': {'base': 'MDT', 'quote': 'USDT'}, 'MITHBTC': {'base': 'MITH', 'quote': 'BTC'},
                            'MITHUSDT': {'base': 'MITH', 'quote': 'USDT'}, 'MKRBTC': {'base': 'MKR', 'quote': 'BTC'},
                            'MKRBUSD': {'base': 'MKR', 'quote': 'BUSD'}, 'MKRUSDT': {'base': 'MKR', 'quote': 'USDT'},
                            'MTLBTC': {'base': 'MTL', 'quote': 'BTC'}, 'MTLUSDT': {'base': 'MTL', 'quote': 'USDT'},
                            'NANOBTC': {'base': 'NANO', 'quote': 'BTC'}, 'NANOBUSD': {'base': 'NANO', 'quote': 'BUSD'},
                            'NANOUSDT': {'base': 'NANO', 'quote': 'USDT'}, 'NBSBTC': {'base': 'NBS', 'quote': 'BTC'},
                            'NBSUSDT': {'base': 'NBS', 'quote': 'USDT'}, 'NEARBTC': {'base': 'NEAR', 'quote': 'BTC'},
                            'NEARUSDT': {'base': 'NEAR', 'quote': 'USDT'}, 'NEOBTC': {'base': 'NEO', 'quote': 'BTC'},
                            'NEOBUSD': {'base': 'NEO', 'quote': 'BUSD'}, 'NEOUSDT': {'base': 'NEO', 'quote': 'USDT'},
                            'NKNBTC': {'base': 'NKN', 'quote': 'BTC'}, 'NKNUSDT': {'base': 'NKN', 'quote': 'USDT'},
                            'NMRBTC': {'base': 'NMR', 'quote': 'BTC'}, 'NMRBUSD': {'base': 'NMR', 'quote': 'BUSD'},
                            'NMRUSDT': {'base': 'NMR', 'quote': 'USDT'}, 'NULSBTC': {'base': 'NULS', 'quote': 'BTC'},
                            'NULSUSDT': {'base': 'NULS', 'quote': 'USDT'},
                            'OCEANBTC': {'base': 'OCEAN', 'quote': 'BTC'},
                            'OCEANBUSD': {'base': 'OCEAN', 'quote': 'BUSD'},
                            'OCEANUSDT': {'base': 'OCEAN', 'quote': 'USDT'}, 'OGNBTC': {'base': 'OGN', 'quote': 'BTC'},
                            'OGNUSDT': {'base': 'OGN', 'quote': 'USDT'}, 'OMGBTC': {'base': 'OMG', 'quote': 'BTC'},
                            'OMGUSDT': {'base': 'OMG', 'quote': 'USDT'}, 'ONEBTC': {'base': 'ONE', 'quote': 'BTC'},
                            'ONEUSDT': {'base': 'ONE', 'quote': 'USDT'}, 'ONGBTC': {'base': 'ONG', 'quote': 'BTC'},
                            'ONGUSDT': {'base': 'ONG', 'quote': 'USDT'}, 'ONTBTC': {'base': 'ONT', 'quote': 'BTC'},
                            'ONTBUSD': {'base': 'ONT', 'quote': 'BUSD'}, 'ONTUSDT': {'base': 'ONT', 'quote': 'USDT'},
                            'ORNBTC': {'base': 'ORN', 'quote': 'BTC'}, 'ORNUSDT': {'base': 'ORN', 'quote': 'USDT'},
                            'OXTBTC': {'base': 'OXT', 'quote': 'BTC'}, 'OXTUSDT': {'base': 'OXT', 'quote': 'USDT'},
                            'PAXGBTC': {'base': 'PAXG', 'quote': 'BTC'}, 'PAXGUSDT': {'base': 'PAXG', 'quote': 'USDT'},
                            'PNTBTC': {'base': 'PNT', 'quote': 'BTC'}, 'PNTUSDT': {'base': 'PNT', 'quote': 'USDT'},
                            'POLYBTC': {'base': 'POLY', 'quote': 'BTC'}, 'QTUMBTC': {'base': 'QTUM', 'quote': 'BTC'},
                            'QTUMBUSD': {'base': 'QTUM', 'quote': 'BUSD'},
                            'QTUMUSDT': {'base': 'QTUM', 'quote': 'USDT'}, 'REEFBTC': {'base': 'REEF', 'quote': 'BTC'},
                            'REEFUSDT': {'base': 'REEF', 'quote': 'USDT'}, 'RENBTC': {'base': 'REN', 'quote': 'BTC'},
                            'RENUSDT': {'base': 'REN', 'quote': 'USDT'}, 'REPBTC': {'base': 'REP', 'quote': 'BTC'},
                            'REPBUSD': {'base': 'REP', 'quote': 'BUSD'}, 'REPUSDT': {'base': 'REP', 'quote': 'USDT'},
                            'RLCBTC': {'base': 'RLC', 'quote': 'BTC'}, 'RLCUSDT': {'base': 'RLC', 'quote': 'USDT'},
                            'ROSEBTC': {'base': 'ROSE', 'quote': 'BTC'}, 'ROSEBUSD': {'base': 'ROSE', 'quote': 'BUSD'},
                            'ROSEUSDT': {'base': 'ROSE', 'quote': 'USDT'}, 'RSRBTC': {'base': 'RSR', 'quote': 'BTC'},
                            'RSRBUSD': {'base': 'RSR', 'quote': 'BUSD'}, 'RSRUSDT': {'base': 'RSR', 'quote': 'USDT'},
                            'RUNEBTC': {'base': 'RUNE', 'quote': 'BTC'}, 'RUNEBUSD': {'base': 'RUNE', 'quote': 'BUSD'},
                            'RUNEUSDT': {'base': 'RUNE', 'quote': 'USDT'}, 'RVNBTC': {'base': 'RVN', 'quote': 'BTC'},
                            'RVNBUSD': {'base': 'RVN', 'quote': 'BUSD'}, 'RVNUSDT': {'base': 'RVN', 'quote': 'USDT'},
                            'SANDBTC': {'base': 'SAND', 'quote': 'BTC'}, 'SANDBUSD': {'base': 'SAND', 'quote': 'BUSD'},
                            'SANDUSDT': {'base': 'SAND', 'quote': 'USDT'}, 'SCBTC': {'base': 'SC', 'quote': 'BTC'},
                            'SCUSDT': {'base': 'SC', 'quote': 'USDT'}, 'SFPBTC': {'base': 'SFP', 'quote': 'BTC'},
                            'SFPBUSD': {'base': 'SFP', 'quote': 'BUSD'}, 'SFPUSDT': {'base': 'SFP', 'quote': 'USDT'},
                            'SKLBTC': {'base': 'SKL', 'quote': 'BTC'}, 'SKLBUSD': {'base': 'SKL', 'quote': 'BUSD'},
                            'SKLUSDT': {'base': 'SKL', 'quote': 'USDT'}, 'SNXBTC': {'base': 'SNX', 'quote': 'BTC'},
                            'SNXBUSD': {'base': 'SNX', 'quote': 'BUSD'}, 'SNXUSDT': {'base': 'SNX', 'quote': 'USDT'},
                            'SOLBTC': {'base': 'SOL', 'quote': 'BTC'}, 'SOLBUSD': {'base': 'SOL', 'quote': 'BUSD'},
                            'SOLUSDT': {'base': 'SOL', 'quote': 'USDT'}, 'SRMBTC': {'base': 'SRM', 'quote': 'BTC'},
                            'SRMBUSD': {'base': 'SRM', 'quote': 'BUSD'}, 'SRMUSDT': {'base': 'SRM', 'quote': 'USDT'},
                            'STMXBTC': {'base': 'STMX', 'quote': 'BTC'}, 'STMXUSDT': {'base': 'STMX', 'quote': 'USDT'},
                            'STORJBTC': {'base': 'STORJ', 'quote': 'BTC'},
                            'STORJBUSD': {'base': 'STORJ', 'quote': 'BUSD'},
                            'STORJUSDT': {'base': 'STORJ', 'quote': 'USDT'},
                            'STPTBTC': {'base': 'STPT', 'quote': 'BTC'}, 'STPTUSDT': {'base': 'STPT', 'quote': 'USDT'},
                            'STXBTC': {'base': 'STX', 'quote': 'BTC'}, 'STXUSDT': {'base': 'STX', 'quote': 'USDT'},
                            'SUSHIBTC': {'base': 'SUSHI', 'quote': 'BTC'},
                            'SUSHIBUSD': {'base': 'SUSHI', 'quote': 'BUSD'},
                            'SUSHIUSDT': {'base': 'SUSHI', 'quote': 'USDT'}, 'SXPBTC': {'base': 'SXP', 'quote': 'BTC'},
                            'SXPBUSD': {'base': 'SXP', 'quote': 'BUSD'}, 'SXPEUR': {'base': 'SXP', 'quote': 'EUR'},
                            'SXPUSDT': {'base': 'SXP', 'quote': 'USDT'}, 'TCTBTC': {'base': 'TCT', 'quote': 'BTC'},
                            'TCTUSDT': {'base': 'TCT', 'quote': 'USDT'}, 'TFUELBTC': {'base': 'TFUEL', 'quote': 'BTC'},
                            'TFUELUSDT': {'base': 'TFUEL', 'quote': 'USDT'},
                            'THETABTC': {'base': 'THETA', 'quote': 'BTC'},
                            'THETAUSDT': {'base': 'THETA', 'quote': 'USDT'},
                            'TOMOBTC': {'base': 'TOMO', 'quote': 'BTC'}, 'TOMOBUSD': {'base': 'TOMO', 'quote': 'BUSD'},
                            'TOMOUSDT': {'base': 'TOMO', 'quote': 'USDT'}, 'TRBBTC': {'base': 'TRB', 'quote': 'BTC'},
                            'TRBBUSD': {'base': 'TRB', 'quote': 'BUSD'}, 'TRBUSDT': {'base': 'TRB', 'quote': 'USDT'},
                            'TROYBTC': {'base': 'TROY', 'quote': 'BTC'}, 'TROYUSDT': {'base': 'TROY', 'quote': 'USDT'},
                            'TRXBTC': {'base': 'TRX', 'quote': 'BTC'}, 'TRXBUSD': {'base': 'TRX', 'quote': 'BUSD'},
                            'TRXETH': {'base': 'TRX', 'quote': 'ETH'}, 'TRXUSDT': {'base': 'TRX', 'quote': 'USDT'},
                            'UMABTC': {'base': 'UMA', 'quote': 'BTC'}, 'UMAUSDT': {'base': 'UMA', 'quote': 'USDT'},
                            'UNFIBTC': {'base': 'UNFI', 'quote': 'BTC'}, 'UNFIBUSD': {'base': 'UNFI', 'quote': 'BUSD'},
                            'UNFIUSDT': {'base': 'UNFI', 'quote': 'USDT'}, 'UNIBTC': {'base': 'UNI', 'quote': 'BTC'},
                            'UNIBUSD': {'base': 'UNI', 'quote': 'BUSD'}, 'UNIUSDT': {'base': 'UNI', 'quote': 'USDT'},
                            'UTKBTC': {'base': 'UTK', 'quote': 'BTC'}, 'UTKUSDT': {'base': 'UTK', 'quote': 'USDT'},
                            'VETBTC': {'base': 'VET', 'quote': 'BTC'}, 'VETBUSD': {'base': 'VET', 'quote': 'BUSD'},
                            'VETUSDT': {'base': 'VET', 'quote': 'USDT'}, 'VITEBTC': {'base': 'VITE', 'quote': 'BTC'},
                            'VITEUSDT': {'base': 'VITE', 'quote': 'USDT'},
                            'VTHOBUSD': {'base': 'VTHO', 'quote': 'BUSD'},
                            'VTHOUSDT': {'base': 'VTHO', 'quote': 'USDT'}, 'WANBTC': {'base': 'WAN', 'quote': 'BTC'},
                            'WANUSDT': {'base': 'WAN', 'quote': 'USDT'}, 'WAVESBTC': {'base': 'WAVES', 'quote': 'BTC'},
                            'WAVESBUSD': {'base': 'WAVES', 'quote': 'BUSD'},
                            'WAVESUSDT': {'base': 'WAVES', 'quote': 'USDT'},
                            'WINGBTC': {'base': 'WING', 'quote': 'BTC'}, 'WINGBUSD': {'base': 'WING', 'quote': 'BUSD'},
                            'WINGUSDT': {'base': 'WING', 'quote': 'USDT'}, 'WNXMBTC': {'base': 'WNXM', 'quote': 'BTC'},
                            'WNXMBUSD': {'base': 'WNXM', 'quote': 'BUSD'},
                            'WNXMUSDT': {'base': 'WNXM', 'quote': 'USDT'}, 'WRXBTC': {'base': 'WRX', 'quote': 'BTC'},
                            'WRXBUSD': {'base': 'WRX', 'quote': 'BUSD'}, 'WRXUSDT': {'base': 'WRX', 'quote': 'USDT'},
                            'WTCBTC': {'base': 'WTC', 'quote': 'BTC'}, 'WTCUSDT': {'base': 'WTC', 'quote': 'USDT'},
                            'XEMBTC': {'base': 'XEM', 'quote': 'BTC'}, 'XEMUSDT': {'base': 'XEM', 'quote': 'USDT'},
                            'XLMBTC': {'base': 'XLM', 'quote': 'BTC'}, 'XLMBUSD': {'base': 'XLM', 'quote': 'BUSD'},
                            'XLMEUR': {'base': 'XLM', 'quote': 'EUR'}, 'XLMUSDT': {'base': 'XLM', 'quote': 'USDT'},
                            'XMRBTC': {'base': 'XMR', 'quote': 'BTC'}, 'XMRBUSD': {'base': 'XMR', 'quote': 'BUSD'},
                            'XMRUSDT': {'base': 'XMR', 'quote': 'USDT'}, 'XRPBTC': {'base': 'XRP', 'quote': 'BTC'},
                            'XRPBUSD': {'base': 'XRP', 'quote': 'BUSD'}, 'XRPETH': {'base': 'XRP', 'quote': 'ETH'},
                            'XRPEUR': {'base': 'XRP', 'quote': 'EUR'}, 'XRPGBP': {'base': 'XRP', 'quote': 'GBP'},
                            'XRPUSDT': {'base': 'XRP', 'quote': 'USDT'}, 'XTZBTC': {'base': 'XTZ', 'quote': 'BTC'},
                            'XTZBUSD': {'base': 'XTZ', 'quote': 'BUSD'}, 'XTZUSDT': {'base': 'XTZ', 'quote': 'USDT'},
                            'XVGBTC': {'base': 'XVG', 'quote': 'BTC'}, 'XVSBTC': {'base': 'XVS', 'quote': 'BTC'},
                            'XVSUSDT': {'base': 'XVS', 'quote': 'USDT'}, 'XZCBTC': {'base': 'XZC', 'quote': 'BTC'},
                            'XZCUSDT': {'base': 'XZC', 'quote': 'USDT'}, 'YFIBTC': {'base': 'YFI', 'quote': 'BTC'},
                            'YFIBUSD': {'base': 'YFI', 'quote': 'BUSD'}, 'YFIEUR': {'base': 'YFI', 'quote': 'EUR'},
                            'YFIIBTC': {'base': 'YFII', 'quote': 'BTC'}, 'YFIIBUSD': {'base': 'YFII', 'quote': 'BUSD'},
                            'YFIIUSDT': {'base': 'YFII', 'quote': 'USDT'}, 'YFIUSDT': {'base': 'YFI', 'quote': 'USDT'},
                            'ZECBTC': {'base': 'ZEC', 'quote': 'BTC'}, 'ZECBUSD': {'base': 'ZEC', 'quote': 'BUSD'},
                            'ZECUSDT': {'base': 'ZEC', 'quote': 'USDT'}, 'ZENBTC': {'base': 'ZEN', 'quote': 'BTC'},
                            'ZENETH': {'base': 'ZEN', 'quote': 'ETH'}, 'ZENUSDT': {'base': 'ZEN', 'quote': 'USDT'},
                            'ZILBTC': {'base': 'ZIL', 'quote': 'BTC'}, 'ZILBUSD': {'base': 'ZIL', 'quote': 'BUSD'},
                            'ZILUSDT': {'base': 'ZIL', 'quote': 'USDT'}, 'ZRXBTC': {'base': 'ZRX', 'quote': 'BTC'},
                            'ZRXBUSD': {'base': 'ZRX', 'quote': 'BUSD'}, 'ZRXUSDT': {'base': 'ZRX', 'quote': 'USDT'}}

indicator_default_options = {
    'SMA (Simple Moving Average)': '(7, Open)',
    'EMA (Exponential Moving Average)': '(7, Open)',
    'WMA (Weighted Moving Average)': '(7, Open)',
    'BOLL - Upper Band (Bollinger Band)': '(21, 2)',
    'BOLL - Lower Band (Bollinger Band)': '(21, 2)',
    'VWAP (Volumen Weighted Average Price)': '(14)',
    'TRIX (Triple Exponential Average)': '(9)',
    'SAR (Stop and Reverse)': '(0.02, 0.2)',
    'MACD - MACD Line (Moving Average Eonvergence Divergence)': '(12, 26, 9, Open)',
    'MACD - Singal Line (Moving Average Eonvergence Divergence)': '(12, 26, 9, Open)',
    'RSI (Relative Strength Index)': '(6)',
    'KDJ (Random Index)': '(9, 3, 3)',
    'OBV (On-balance volume)': '(-)',
    'CCI (Commodity Channel Index)': '(20)',
    'StochRSI (Stoch Relative Strength Index)': '(14, 14)',
    'WR (Williams %)': '(14)',
    'DMI (Directional Movement Index)': '(14)',
    'MTM (Momentum)': '(14, Close)',
    'EMV (Ease of Movement)': '(14, 10000)',
    'Value (Plain integer or double)': '(0)',
    'Open (Open price of candle)': '(-)',
    'High (High price of candle)': '(-)',
    'Low (Low price of candle)': '(-)',
    'Close (Close price of candle)': '(-)',
    'Volume (Amount traded in amount of time)': '(-)'
}

indicator_options_name = {
'SMA (Simple Moving Average)': ['Length', 'Source'],
    'EMA (Exponential Moving Average)': ['Length', 'Source'],
    'WMA (Weighted Moving Average)': ['Length', 'Source'],
    'BOLL - Upper Band (Bollinger Band)': ['Length', 'Multiplier'],
    'BOLL - Lower Band (Bollinger Band)': ['Length', 'Multiplier'],
    'VWAP (Volumen Weighted Average Price)': ['Length'],
    'TRIX (Triple Exponential Average)': ['Length'],
    'SAR (Stop and Reverse)': ['Start', 'Maximum'],
    'MACD - MACD Line (Moving Average Eonvergence Divergence)': ['Fast Length', 'Slow Length', 'Signal Length', 'Source'],
    'MACD - Singal Line (Moving Average Eonvergence Divergence)': ['Fast Length', 'Slow Length', 'Signal Length', 'Source'],
    'RSI (Relative Strength Index)': ['Length'],
    'KDJ (Random Index)': ['Length', 'K%', 'D%'],
    'OBV (On-balance volume)': [],
    'CCI (Commodity Channel Index)': ['Length'],
    'StochRSI (Stoch Relative Strength Index)': ['LengthRSI', 'LengthStoch'],
    'WR (Williams %)': ['Length'],
    'DMI (Directional Movement Index)': ['Length'],
    'MTM (Momentum)': ['Length', 'Source'],
    'EMV (Ease of Movement)': ['Length', 'Divisor'],
    'Value (Plain integer or double)': ['Plain value'],
    'Open (Open price of candle)': [],
    'High (High price of candle)': [],
    'Low (Low price of candle)': [],
    'Close (Close price of candle)': [],
    'Volume (Amount traded in amount of time)': []
}

month_dictionary = {
    '01': 'January',
    '02': 'February',
    '03': 'March',
    '04': 'April',
    '05': 'May',
    '06': 'June',
    '07': 'July',
    '08': 'August',
    '09': 'September',
    '10': 'October',
    '11': 'November',
    '12': 'December'
}

difference_period_dictionary = {
    60000: '1m',
    180000: '3m',
    300000: '5m',
    900000: '15m',
    1800000: '30m',
    3600000: '1h',
    7200000: '2h',
    14400000: '4h',
    21600000: '6h',
    28800000: '8h',
    43200000: '12h',
    86400000: '1d',
    259200000: '3d',
    604800000: '1w'
}