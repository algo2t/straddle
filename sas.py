from alphatrade import *
import config
import datetime as datetime
import pandas as pd
import requests
from alphatrade import AlphaTrade

sas = AlphaTrade(login_id=config.login_id, password=config.password, twofa=config.twofa, access_token=config.access_token, master_contracts_to_download=['NFO'])


def get_symbol_ce(symbol,d,m,y,strike):
    x=sas.get_instrument_for_fno(symbol = symbol, expiry_date=datetime.date(y, m, d), is_fut=False, strike=strike, is_call = True)
    return str(x.symbol)
def get_symbol_pe(symbol,d,m,y,strike):
    x=sas.get_instrument_for_fno(symbol = symbol, expiry_date=datetime.date(y, m, d), is_fut=False, strike=strike, is_call = False)
    return str(x.symbol)


def intraday(script,interval):
    return sas.get_intraday_candles('NFO', script, interval=interval)

def vwap(ce,pe):
    q=ce['volume']+pe['volume']
    p=ce['close']+pe['close']
    return ((p * q).cumsum() / q.cumsum())


def get_token_ce(symbol,d,m,y,strike):
    x=sas.get_instrument_for_fno(symbol = symbol, expiry_date=datetime.date(y, m, d), is_fut=False, strike=strike, is_call = True)
    return str(x.token)
def get_token_pe(symbol,d,m,y,strike):
    x=sas.get_instrument_for_fno(symbol = symbol, expiry_date=datetime.date(y, m, d), is_fut=False, strike=strike, is_call = False)
    return str(x.token)
#data['close'].to_csv('int.csv', index=True,header=False)
#print(data['close'])
#data=pd.read_csv('int.csv', usecols=['close']).T.values.tolist()[0]
#print(data)