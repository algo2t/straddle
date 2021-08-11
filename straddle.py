import sas
import ltp
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import plotly.graph_objects as go
from datetime import datetime

time_intervals=[1,2,3,4,5,7,10]
date=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,29,30,31]
month=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
today = datetime.today()
start_time = (datetime(today.year, today.month,
                                  today.day, hour=9, minute=00))
chart=st.empty()
chart1=st.empty()
symbols=['BANKNIFTY','FINNIFTY','NIFTY','ACC','ASHOKLEY','ALKEM','APLLTD','APOLLOHOSP','AUROPHARMA','BERGEPAINT','AARTIIND','BHEL','ABFRL','ADANIENT','AMBUJACEM','ADANIPORTS','AUBANK','AXISBANK','BAJAJ-AUTO','BAJAJFINSV','BAJFINANCE','ASIANPAINT','BANDHANBNK','BANKBARODA','BEL','CADILAHC','CANBK','CIPLA','COALINDIA','COFORGE','COLPAL','CUMMINSIND','DABUR','DEEPAKNTR','DRREDDY','EICHERMOT','ESCORTS','EXIDEIND','FEDERALBNK','GLENMARK','GMRINFRA','GODREJCP','GRASIM','BHARTIARTL','HDFC','HDFCAMC','HDFCBANK','HDFCLIFE','HINDALCO','COROMANDEL','ICICIBANK','ICICIGI','ICICIPRULI','IDEA','IDFCFIRSTB','IGL','INDIGO','INDUSINDBK','INDUSTOWER','IRCTC','ITC','JINDALSTEL','JSWSTEEL','KOTAKBANK','L&TFH','LICHSGFIN','LTTS','M&M','M&MFIN','MANAPPURAM','MARICO','HCLTECH','HINDPETRO','MCDOWELL-N','MGL','IBULHSGFIN','MINDTREE','MPHASIS','MRF','MUTHOOTFIN','NATIONALUM','NESTLEIND','NMDC','NTPC','PAGEIND','PFC','PIDILITIND','PIIND','POWERGRID','INDHOTEL','PVR','RBLBANK','RECLTD','INFY','JUBLFOOD','RELIANCE','SBIN','SHREECEM','SRTRANSFIN','SUNPHARMA','SUNTV','TATACHEM','TATAPOWER','TCS','TITAN','TVSMOTOR','UBL','MARUTI','ULTRACEMCO','UPL','VEDL','METROPOLIS','MFSL','BALKRISIND','GRANULES','NAVINFLUOR','APOLLOTYRE','PFIZER','BIOCON','SAIL','BOSCHLTD','BRITANNIA','CHOLAFIN','CONCOR','CUB','SBILIFE','DIVISLAB','DLF','GAIL','SRF','GUJGASLTD','HAVELLS','HINDUNILVR','IOC','LALPATHLAB','LT','LUPIN','MOTHERSUMI','NAM-INDIA','NAUKRI','RAMCOCEM','SIEMENS','TATACONSUM','TATASTEEL','TORNTPHARM','TORNTPOWER','TRENT','LTI','BHARATFORG','ONGC','TECHM','VOLTAS','WIPRO','ZEEL','GODREJPROP','BATAINDIA','HEROMOTOCO','PEL','PNB','TATAMOTORS','AMARAJABAT','BPCL','PETRONET','ASTRAL','STAR']
interval=st.sidebar.selectbox("Time frame (min.)",time_intervals)
symbol=st.sidebar.selectbox("Symbol",symbols)
strike=st.sidebar.text_input("Strike")
d=st.sidebar.selectbox("Expiry Date",date)
m=st.sidebar.selectbox("Expiry Month",month)
y=2021


if st.sidebar.button("Submit"):
    strike=int(strike)
    while True:

        ce=sas.get_symbol_ce(symbol.upper(),d,m,y,strike)
        ce_ltp=sas.intraday(ce,interval)
    #st.write(ce_ltp['close'])

        pe=sas.get_symbol_pe(symbol.upper(),d,m,y,strike)
        pe_ltp=sas.intraday(pe,interval)

        straddle_ltp=ltp.get_ltp(sas.get_token_ce(symbol.upper(),d,m,y,strike))+ltp.get_ltp(sas.get_token_pe(symbol.upper(),d,m,y,strike))
        #print(straddle_ltp)
    #st.write(pe_ltp['close'])

        straddle=ce_ltp['close']+pe_ltp['close']
        st.write(straddle)
        st.write(start_time)
        #chart._arrow_line_chart(straddle)
        fig = px.line(straddle, x=straddle.index, y="close", title=str(symbol)+'-Straddle-'+str(strike)+str("-Expiry-(")+str(d)+str("/")+str(m)+str(")  Current premium=")+str(straddle_ltp))
        fig.add_scatter(x=straddle.index, y=sas.vwap(ce_ltp,pe_ltp), mode='lines',name="vwap")
        
        fig1 = go.Figure(data=go.Candlestick(x=straddle.index,
                open=ce_ltp['open']+pe_ltp['open'],
                high=ce_ltp['high']+pe_ltp['high'],
                low=ce_ltp['low']+pe_ltp['low'],
                close=ce_ltp['close']+pe_ltp['close']))
        #fig.show()
        fig1.add_scatter(x=straddle.index, y=sas.vwap(ce_ltp,pe_ltp), mode='lines',name='vwap')
        chart.plotly_chart(fig)
        chart1.plotly_chart(fig1)
        time.sleep(5)