# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 09:31:20 2025

@author: PALDEN
"""

import streamlit as st 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px 


company_list =[
    r'C:\\Users\\rocke\\Downloads\\S&P\\individual_stocks_5yr\\MSFT_data.csv',
    r'C:\\Users\\rocke\\Downloads\\S&P\\individual_stocks_5yr\\GOOG_data.csv',
    r'C:\\Users\\rocke\\Downloads\\S&P\\individual_stocks_5yr\\AMGN_data.csv',
    r'C:\\Users\\rocke\\Downloads\\S&P\\individual_stocks_5yr\\AAP_data.csv'
 
]

all_data = pd.DataFrame()
for file in company_list:
    current_df = pd.read_csv(file)
    all_data =pd.concat([all_data,current_df],ignore_index=True)
    
all_data['date'] = pd.to_datetime(all_data['date'])   


st.set_page_config(page_title = "Stock Analysis Dashboard", layout="wide")
st.title("Tech Stocks Analysis Dashboard")

tech_list = all_data['Name'].unique()
st.sidebar.title("Choose a Company")
selected_company = st.sidebar.selectbox("Select a stock",tech_list)

#company_df = all_data['Name']==selected_company
#company_df.sort_values('date', inplace=True)
company_df = all_data[all_data['Name'] == selected_company]
company_df.sort_values(by='date', inplace=True)


## 1st plot:
st.subheader(f'1. Closing prices of {selected_company} over time')
fig1 = px.line(company_df,x='date', y='close', title = selected_company + "closing prices over time" )
st.plotly_chart(fig1 , use_container_width = True)

## 2nd plot:
st.subheader("2. Moving Average (10, 20, 50 days")
ma_day = [10, 20, 50]
for ma in ma_day:
    company_df['close' +str(ma)] = company_df['close'].rolling(ma).mean()
    
fig2 = px.line(company_df,x='date', y=['close','close10', 'close20',
       'close50'], title = selected_company + "closing prices with moving average" )
st.plotly_chart(fig2 , use_container_width = True)


## 3rd plot:
st.subheader("3. Daily return for" + selected_company)
company_df['Daily Return(%)'] = company_df['close'].pct_change() * 100
fig3 = px.line(company_df,x='date', y='Daily Return(%)', title = 'Daily Return(%)' )
st.plotly_chart(fig3 , use_container_width = True)


## 4th plot:
st.subheader("4. Resampled Closing Price (/Monthly/Quarterly/Yearly)")

company_df.set_index('date', inplace=True)
#radio button
Resample_option = st.radio("Select Resample Frequency", ["monthly", "Quarterly","Yearly"])

if Resample_option == "Monthly":
    resampled = company_df['close'].resample('M').mean()
elif Resample_option == "Quarterly":
    resampled = company_df['close'].resample('Q').mean()
else:
    resampled = company_df['close'].resample('Y').mean()
    
    resampled = resampled.reset_index()
resampled.columns = ['date', 'average_close']

#fig4 = px.line(resampled, title = selected_company + " " + Resample_option + "Average closing price")
#st.plotly_chart(fig4 , use_container_width = True)
fig4 = px.line(
    resampled,
    x='date',
    y='average_close',
    title=f"{selected_company} {Resample_option} Average Closing Price"
)

st.plotly_chart(fig4, use_container_width=True)


## 5th plot:
    
msft = pd.read_csv(company_list[0])
amzn = pd.read_csv(company_list[1])
google = pd.read_csv(company_list[2])
app = pd.read_csv(company_list[3])

closing_price = pd.DataFrame()

closing_price['msft_close'] = msft['close']
closing_price['amzn_close'] = amzn['close']
closing_price['google_close'] = google['close']
closing_price['app_close'] = app['close']

fig5, ax = plt.subplots()
sns.heatmap(closing_price.corr(), annot = True, cmap="coolwarm", ax=ax)
st.pyplot(fig5)

st.markdown("---")
st.markdown("**Note:** This dashboard provides basic technical analysis of major tech stocks using Python")

