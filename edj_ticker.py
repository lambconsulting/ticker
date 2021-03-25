# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 10:41:28 2021

@author: lamb0
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 21:36:25 2020

@author: lamb0
"""

import tabulate
import os
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
today = datetime.today().strftime("%Y-%m-%d")

tpath = "C://Users//lamb0//Downloads//"
fn="edj_ticker_20210325"
extension='.xlsx'
file = tpath+fn+extension
file
edj = pd.read_excel((file), sheet_name='UPD')
edj.rename(columns = {'SYMBOL/CUSIP':'ticker','SHARES':'vol'}, inplace = True) 
type(edj)
print(edj)

#Get string of tickers prior to transpose to feed through Yahoo Finance API
t_string = edj['ticker'].to_string(index=False)
# Get list of tickers for plotting
t_list = edj.ticker.tolist()
#Resume with transpose for array like tickers price and volume calculation
edj['ticker'] = edj.ticker+"_v"
edj = edj.set_index('ticker').T
edj['key'] = 0
print(edj)
type(edj)


#for cols in t_string:
#    print(cols)
#bny_edj.columns


yf_in = yf.download(t_string, start="2020-12-01", end=today)
yf_dl = yf_in.drop(['Low','Open','High', 'Volume', 'Adj Close'], axis=1, level=0)
yf_dl.columns = yf_dl.columns.droplevel(0)
yf_dl['date'] = yf_dl.index
yf_dl['key'] = 0
data = yf_dl.merge(edj, how='outer', on ='key')
print(data)



# Make calculation for amount by multiplying price by volume
for i in t_list:
    data[i+(str("_amt"))] = data[i] * data[i+(str("_v"))]
data.to_csv('C:\Junk\out.csv', index=False) 
# Plot ticker closing amount based upon volume purchased
for i in t_list:
    data.plot(x='date',y=(["SPY_amt",i+(str("_amt"))]),color=(['black','red']),
              secondary_y=[i+(str("_amt"))])
    
with PdfPages('C:\Junk\m_ticker_volume.pdf') as pdf:
    plt.figure(figsize=(3, 3))
    for i in t_list:
        data.plot(x='date',y=(["SPY_amt",i+(str("_amt"))]),color=(['black','red']),
                  secondary_y=[i+(str("_amt"))])
        plt.title("SPY"+" "+i)
        pdf.savefig() # saves the current figure into a pdf page
        plt.close()
        
# Plot ticker closing price as listed
for i in t_list:
    data.plot(x='date',y=(["SPY",i]),color=(['black','red']),
              secondary_y=[i])
 
# Plot ticker closing price as listed to PDF   
with PdfPages('C:\Junk\m_ticker_only.pdf') as pdf:
    plt.figure(figsize=(3, 3))
    for i in t_list:
        data.plot(x='date',y=(["SPY",i]),color=(['black','red']),
                  secondary_y=[i])
        plt.title("SPY"+" "+i)
        pdf.savefig() # saves the current figure into a pdf page
        plt.close()
    


