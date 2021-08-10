from alphatrade import *
import config
import datetime as datetime
import pandas as pd
import requests
from alphatrade import AlphaTrade
from datetime import datetime as dt

sas = AlphaTrade(login_id=config.login_id, password=config.password, twofa=config.twofa, access_token=config.access_token, master_contracts_to_download=['NFO'])


def get_symbol_ce(symbol,date,strike):
    x=sas.get_instrument_for_fno(symbol = symbol, expiry_date=date, is_fut=False, strike=strike, is_call = True)
    return str(x.symbol)
def get_symbol_pe(symbol,date,strike):
    x=sas.get_instrument_for_fno(symbol = symbol, expiry_date=date, is_fut=False, strike=strike, is_call = False)
    return str(x.symbol)


def intraday(script,interval,startdate):
    x1=sas.get_historical_candles('NFO', script,startdate,dt.now(), interval=interval)
    x2=sas.get_intraday_candles('NFO', script, interval=interval)
    return pd.concat([x1,x2])

def vwap(ce,pe):
    q=ce['volume']+pe['volume']
    p=ce['close']+pe['close']
    return ((p * q).cumsum() / q.cumsum())


def get_token_ce(symbol,date,strike):
    x=sas.get_instrument_for_fno(symbol = symbol, expiry_date=date, is_fut=False, strike=strike, is_call = True)
    return str(x.token)
def get_token_pe(symbol,date,strike):
    x=sas.get_instrument_for_fno(symbol = symbol, expiry_date=date, is_fut=False, strike=strike, is_call = False)
    return str(x.token)
#data['close'].to_csv('int.csv', index=True,header=False)
#print(data['close'])
#data=pd.read_csv('int.csv', usecols=['close']).T.values.tolist()[0]
#print(data)