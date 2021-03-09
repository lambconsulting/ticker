# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 21:36:25 2020

@author: lamb0
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime
today = datetime.today().strftime("%Y-%m-%d")

# EDJ
edj = pd.read_csv("C:/Users/lamb0/Downloads/s1.csv", usecols=[1,4],skiprows=[0,1,2])
edj.dropna(inplace=True)
edj.rename(columns = {'SYMBOL/CUSIP':'ticker','SHARES':'vol'}, inplace = True) 
type(edj)
print(edj)

#BNY Tickers Cleanup
bny_t = pd.read_csv("C:/Users/lamb0/Downloads/s2.csv", usecols=[0],skiprows=[0,1])
bny_t = bny_t.astype(str) # Transform as character.
type(bny_t)
bny_t['countme'] = 1
bny_t['countme'] = bny_t['countme'].cumsum()
type(bny_t)
print(bny_t)

#BNY Volume Cleanup
bny_all = pd.read_csv("C:/Users/lamb0/Downloads/s2.csv", usecols=[0,6],skiprows=[0,1])
vol = bny_all['Quantity'].str.replace(',', '').astype(float).astype(int)
#vol.rename(columns = {'Quantity':'vol'}, inplace = True)
vol = pd.DataFrame([vol])
vol = vol.transpose()
vol['countme'] = 1
vol['countme'] = vol['countme'].cumsum()
type(vol)
print(vol)

# BNY Merge Tickers and Volume
bny = bny_t.merge(vol, how='outer', on ='countme')
bny.rename(columns = {'Security ID':'ticker', 'Quantity':'vol'}, inplace = True) 

#bny = bny.drop(['countme'], axis=1)
bny = bny.drop(columns=['countme']) # Does same thing as axis = 1
bny = bny.groupby('ticker', as_index=False).sum()
print(bny)


bny_edj = bny.append(edj)
bny_edj = bny_edj[~bny_edj.ticker.isin( ['MFRS','GOFXX','DUS','CASH'])]
#Get string of tickers prior to transpose to feed through Yahoo Finance API
t_string = bny_edj['ticker'].to_string(index=False)
# Get list of tickers for plotting
t_list = bny_edj.ticker.tolist()
#Resume with transpose for array like tickers price and volume calculation
bny_edj['ticker'] = bny_edj.ticker+"_v"
bny_edj = bny_edj.set_index('ticker').T
bny_edj['key'] = 0
print(bny_edj)
type(bny_edj)


#for cols in t_string:
#    print(cols)
#bny_edj.columns


yf_in = yf.download(t_string, start="2020-12-01", end=today)
yf_dl = yf_in.drop(['Low','Open','High', 'Volume', 'Adj Close'], axis=1, level=0)
yf_dl.columns = yf_dl.columns.droplevel(0)
yf_dl['date'] = yf_dl.index
yf_dl['key'] = 0
#data1 = data.merge(df_vol, how='outer', on ='key')
data = yf_dl.merge(bny_edj, how='outer', on ='key')
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
    


