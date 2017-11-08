
"""
Created on Wed Oct 18 11:01:17 2017

@author: slai
"""

#Does demand for green taxi's increase or decrease by season? Can we predict demand (initiated rides) based on season?
#Can we predict ride distance based on season?
#Import pandas and dataset
#%%
import pandas as pd
import datetime as dt
import numpy as np
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(font_scale=1.5)
#%%
url = '2016_Green_Taxi_Trip_Data.csv'
dftaxi = pd.read_csv(url,encoding="utf-8-sig")
#%%
dftaxi.head()
print(dftaxi.dtypes)
#%% Ensure data quality. Do not have incorrect long's in dataset. 
dftaxi[dftaxi['Pickup_longitude'] > 0]   
#%% QC to check the differences between lat/long and response variable. 7M row discrepancy. 
dftaxi.count()
#%% Parse date from datetime
#dftaxi.iloc[0]['lpep_pickup_datetime'].split(" ")
dftaxi['pickup_timestring'] = dftaxi['lpep_pickup_datetime'].apply(lambda x: x.split(" ")[0]) #pickup_timestring
dftaxi['dropoff_timestring'] = dftaxi['Lpep_dropoff_datetime'].apply(lambda x: x.split(" ")[0]) #dropoff_timestring
#%% Assign Response variable
dftaxi['response_variable'] = np.where(dftaxi.pickup_timestring is not None & dftaxi.dropoff_timestring is not None, '1',0)
                           #np.where(dftaxi.Lpep_dropoff_datetime is not None,'Dropped off',0))
#dftaxi['location_response'] = np.where(dftaxi.Pickup_longitude< 0, '1',0)
dftaxi.head()
#%% Check to ensure that all rows have a response variable
dftaxi[dftaxi['response_variable'] == '0'] 
#returns empty dataframe! 
#%% Get month out of timestring 
dftaxi['pickup_timestring_month'] = dftaxi['pickup_timestring'].apply(lambda x: x.split("/")[0]) #pickup_timestring_month
#dftaxi['dropoff_timestring_month'] = dftaxi['dropoff_timestring'].apply(lambda x: x.split("/")[0]) #dropoff_timestring_month
#dftaxi[['pickup_timestring','dropoff_timestring']] = dftaxi[['pickup_timestring','dropoff_timestring']].apply(pd.to_datetime)
print(dftaxi.head())
#%% Get Day out of timestring
dftaxi['pickup_timestring_day'] = dftaxi['pickup_timestring'].apply(lambda x: x.split("/")[1]) #pickup_timestring_day
#dftaxi['dropoff_timestring_day'] = dftaxi['dropoff_timestring'].apply(lambda x: x.split("/")[1]) #dropoff_timestring_day
#%%
dftaxi.head()
#%% Subset to relevant columns.
dftaxi = dftaxi[['pickup_timestring','Passenger_count','Trip_distance','Total_amount','response_variable']] # Add response variable
print(dftaxi.head())
print(dftaxi.dtypes)
#%% Convert to numeric
#dftaxi['Total_amount']=dftaxi['Total_amount'].apply(pd.to_numeric)
dftaxi[['Total_amount','response_variable']] = dftaxi[['Total_amount','response_variable']].convert_objects(convert_numeric=True) #deprecated, yet works
#dftaxi['response_variable']=dftaxi['response_variable'].apply(pd.to_numeric)
#dftaxi['pickup_timestring'] = dftaxi['pickup_timestring'].convert_objects(convert_dates=True)

print(dftaxi.dtypes)
#%% Group by day
dftaxi_day = dftaxi[['pickup_timestring','Passenger_count','Trip_distance','Total_amount','response_variable']]
dftaxi_day = dftaxi_day.groupby(['pickup_timestring'],as_index=False).sum()
#dftaxi.groupby(['pickup_timestring'],as_index=False).sum() Old Method. 
print(dftaxi_day.head())
print(dftaxi_day.dtypes)
print('Number of rows in daily aggregated view', len(dftaxi_day))
#%% Convert to date_time and set index
dftaxi_day['pickup_timestring']= pd.to_datetime(dftaxi_day['pickup_timestring'])
dftaxi_day.set_index('pickup_timestring',inplace=True)
#%%

##%% Export clean file to CSV
dftaxi_day.to_csv('dftaxi_by_day.csv',sep=',',index=False,header=True)
##%% Start here to import clean and aggregated data
#url = 'dftaxi_by_day.csv'
#dftaxi_day = pd.read_csv(url,skipinitialspace=True)
#%% 

#%% Trends in daily data. Defaults to index for x
dftaxi_day.plot(y='response_variable',kind='line')
#%% Autocorrelation
print (dftaxi_day.response_variable.autocorr(lag=1)) # 0.65
print (dftaxi_day.response_variable.autocorr(lag=7)) # 0.79
print (dftaxi_day.response_variable.autocorr(lag=21)) # 0.78
print (dftaxi_day.response_variable.autocorr(lag=28)) # 0.80
print (dftaxi_day.response_variable.autocorr(lag=52)) # -0.12
%matplotlib inline
from pandas.plotting import autocorrelation_plot
plot_acf = autocorrelation_plot(dftaxi_day.response_variable)
#%%
#find ideal lag. Cyclical spokes means we have a cycle
from statsmodels.graphics.tsaplots import plot_acf
#from pandas.core import datetools
plot_acf(dftaxi_day.response_variable, lags=52)

#%% Stationariaty
from statsmodels.tsa.arima_model import ARMA
from statsmodels.tsa.arima_model import ARIMA
dftaxi_day = dftaxi_day[['response_variable']].astype(float)
model = ARMA(dftaxi_day, (1, 0)).fit()
model.summary()
#Matches autocorr(1), therefore stationary dataset!
#%%  Residuals for AR(1)
type(model.resid)
print(model.resid.plot())
print(plot_acf(model.resid, lags = 50))
#%% ARMA
arima_model = ARIMA(dftaxi_day, (28,1, 1)).fit()
arima_model.summary()
print(arima_model.resid.plot())
print(plot_acf(arima_model.resid, lags = 50))
#%% Predict
#arima_model.predict(1,100).plot()

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax = dftaxi_day.plot(ax=ax)

fig = arima_model.plot_predict(1, 200, ax=ax, plot_insample=False)