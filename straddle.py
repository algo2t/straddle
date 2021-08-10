import sas
import streamlit as st
import pandas as pd
import plotly.express as px
import time
import plotly.graph_objects as go


time_intervals=[1,3,5,10,15]
date=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,29,30,31]
month=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

chart=st.empty()
chart1=st.empty()
symbols=['NIFTY','BANKNIFTY']
interval=st.sidebar.selectbox("Time interval",time_intervals)
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
    #st.write(pe_ltp['close'])

        straddle=ce_ltp['close']+pe_ltp['close']
        
        #chart._arrow_line_chart(straddle)
        fig = px.line(straddle, x=straddle.index, y="close", title='Straddle- '+str(strike)+str("-Expiry-")+str(d)+str("/")+str(m))
        fig1 = go.Figure(data=go.Candlestick(x=straddle.index,
                open=ce_ltp['open']+pe_ltp['open'],
                high=ce_ltp['high']+pe_ltp['high'],
                low=ce_ltp['low']+pe_ltp['low'],
                close=ce_ltp['close']+pe_ltp['close']))
        #fig.show()
        chart.plotly_chart(fig)
        chart1.plotly_chart(fig1)
        time.sleep(30)