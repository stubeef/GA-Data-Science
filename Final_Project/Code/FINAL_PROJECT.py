
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
dftaxi = pd.read_csv(url)
#%%
dftaxi.head()
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
dftaxi = dftaxi[['pickup_timestring','pickup_timestring_month','pickup_timestring_day','Passenger_count','Trip_distance','Total_amount','response_variable']] # Add response variable
print(dftaxi.head())
print(dftaxi.dtypes)
#%% Convert to numeric
#dftaxi['Total_amount']=dftaxi['Total_amount'].apply(pd.to_numeric)
dftaxi[['Total_amount','response_variable']] = dftaxi[['Total_amount','response_variable']].convert_objects(convert_numeric=True) #deprecated, yet works
#dftaxi['response_variable']=dftaxi['response_variable'].apply(pd.to_numeric)
#dftaxi['pickup_timestring'] = dftaxi['pickup_timestring'].apply(pd.to_datetime)
print(dftaxi.dtypes)
#%% Group by day
dftaxi_day = dftaxi[['pickup_timestring','pickup_timestring_month','pickup_timestring_day','Passenger_count','Trip_distance','Total_amount','response_variable']]
dftaxi_day = dftaxi_day.groupby(['pickup_timestring','pickup_timestring_month','pickup_timestring_day'],as_index=False).sum()
#dftaxi.groupby(['pickup_timestring'],as_index=False).sum() Old Method. 
print(dftaxi_day.head())
print('Number of rows in daily aggregated view', len(dftaxi_day))
#%%
print(dftaxi_day.head())
#%% Export clean file to CSV
dftaxi_day.to_csv('dftaxi_by_day.csv',sep=',',index=False,header=True)
#%% 
dftaxi_day.head()
#%% Patterns in daily data 
dftaxi_day.plot(x='pickup_timestring_month', y='response_variable',kind='line')