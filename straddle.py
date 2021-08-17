import datetime
import sas
import ltp
import streamlit as st
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import time
import plotly.graph_objects as go
from datetime import datetime as dt

time_intervals=[1,2,3,4,5,7,10,15,30,60]
date=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,29,30,31]
st.write("Press stop to analyse click on traces on graph side to hide ")
month=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

startdate=st.sidebar.date_input("Start Date",dt.now())
startdate=datetime.datetime.combine(startdate, datetime.time.min)
chart=st.empty()
chart1=st.empty()
symbols=['BANKNIFTY','FINNIFTY','NIFTY','ACC','ASHOKLEY','ALKEM','APLLTD','APOLLOHOSP','AUROPHARMA','BERGEPAINT','AARTIIND','BHEL','ABFRL','ADANIENT','AMBUJACEM','ADANIPORTS','AUBANK','AXISBANK','BAJAJ-AUTO','BAJAJFINSV','BAJFINANCE','ASIANPAINT','BANDHANBNK','BANKBARODA','BEL','CADILAHC','CANBK','CIPLA','COALINDIA','COFORGE','COLPAL','CUMMINSIND','DABUR','DEEPAKNTR','DRREDDY','EICHERMOT','ESCORTS','EXIDEIND','FEDERALBNK','GLENMARK','GMRINFRA','GODREJCP','GRASIM','BHARTIARTL','HDFC','HDFCAMC','HDFCBANK','HDFCLIFE','HINDALCO','COROMANDEL','ICICIBANK','ICICIGI','ICICIPRULI','IDEA','IDFCFIRSTB','IGL','INDIGO','INDUSINDBK','INDUSTOWER','IRCTC','ITC','JINDALSTEL','JSWSTEEL','KOTAKBANK','L&TFH','LICHSGFIN','LTTS','M&M','M&MFIN','MANAPPURAM','MARICO','HCLTECH','HINDPETRO','MCDOWELL-N','MGL','IBULHSGFIN','MINDTREE','MPHASIS','MRF','MUTHOOTFIN','NATIONALUM','NESTLEIND','NMDC','NTPC','PAGEIND','PFC','PIDILITIND','PIIND','POWERGRID','INDHOTEL','PVR','RBLBANK','RECLTD','INFY','JUBLFOOD','RELIANCE','SBIN','SHREECEM','SRTRANSFIN','SUNPHARMA','SUNTV','TATACHEM','TATAPOWER','TCS','TITAN','TVSMOTOR','UBL','MARUTI','ULTRACEMCO','UPL','VEDL','METROPOLIS','MFSL','BALKRISIND','GRANULES','NAVINFLUOR','APOLLOTYRE','PFIZER','BIOCON','SAIL','BOSCHLTD','BRITANNIA','CHOLAFIN','CONCOR','CUB','SBILIFE','DIVISLAB','DLF','GAIL','SRF','GUJGASLTD','HAVELLS','HINDUNILVR','IOC','LALPATHLAB','LT','LUPIN','MOTHERSUMI','NAM-INDIA','NAUKRI','RAMCOCEM','SIEMENS','TATACONSUM','TATASTEEL','TORNTPHARM','TORNTPOWER','TRENT','LTI','BHARATFORG','ONGC','TECHM','VOLTAS','WIPRO','ZEEL','GODREJPROP','BATAINDIA','HEROMOTOCO','PEL','PNB','TATAMOTORS','AMARAJABAT','BPCL','PETRONET','ASTRAL','STAR']
interval=st.sidebar.selectbox("Time frame (min.)",time_intervals)
symbol=st.sidebar.selectbox("Symbol",symbols)
ma=st.sidebar.text_input("Enter MA period",0)
ce_strike=st.sidebar.text_input("CE Strike")
pe_strike=st.sidebar.text_input("PE Strike")
expiry=st.sidebar.date_input("Expiry Date")



if st.sidebar.button("Submit"):
    ce_strike=int(ce_strike)
    pe_strike=int(pe_strike)
    ma=int(ma)
    while True:

        ce=sas.get_symbol_ce(symbol.upper(),expiry,ce_strike)
        ce_ltp=sas.intraday(ce,interval,startdate)
    #st.write(ce_ltp['close'])

        pe=sas.get_symbol_pe(symbol.upper(),expiry,pe_strike)
        pe_ltp=sas.intraday(pe,interval,startdate)

        straddle_ltp=ltp.get_ltp(sas.get_token_ce(symbol.upper(),expiry,ce_strike))+ltp.get_ltp(sas.get_token_pe(symbol.upper(),expiry,pe_strike))
        #print(straddle_ltp)
    #st.write(pe_ltp['close'])

        straddle=ce_ltp['close']+pe_ltp['close']
        ma_plot=sas.calculate_ma(straddle,ma)
        #chart._arrow_line_chart(straddle)
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.update_layout(
    title_text=" "+str(ce_strike)+"CE   "+str(pe_strike)+"PE   Total Premium="+str(straddle_ltp)
)
        
        fig.add_scatter(x=straddle.index, y=straddle, mode='lines',name="Straddle")
        fig.add_scatter(x=straddle.index, y=sas.vwap(ce_ltp,pe_ltp), mode='lines',name="vwap")
                            
        fig.add_scatter(x=straddle.index, y=ma_plot, mode='lines',name="MA"+str(ma))
        fig.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[15.5, 9.1], pattern="hour"),  # hide hours outside of 9.30am-4pm
            # dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
        ]
    )
       
        fig1 = go.Figure(data=go.Candlestick(x=straddle.index,
                open=ce_ltp['open']+pe_ltp['open'],
                high=ce_ltp['high']+pe_ltp['high'],
                low=ce_ltp['low']+pe_ltp['low'],
                close=ce_ltp['close']+pe_ltp['close']))

        #fig.show()
        fig1.add_scatter(x=straddle.index, y=sas.vwap(ce_ltp,pe_ltp), mode='lines',name='vwap')

        fig1.update_xaxes(
        rangeslider_visible=True,
        rangebreaks=[
            # NOTE: Below values are bound (not single values), ie. hide x to y
            dict(bounds=["sat", "mon"]),  # hide weekends, eg. hide sat to before mon
            dict(bounds=[15.5, 9.1], pattern="hour"),  # hide hours outside of 9.30am-4pm
            # dict(values=["2019-12-25", "2020-12-24"])  # hide holidays (Christmas and New Year's, etc)
        ]
    )
        chart.plotly_chart(fig)
        chart1.plotly_chart(fig1)
        
        time.sleep(2)


