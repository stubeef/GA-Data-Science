# -*- coding: utf-8 -*-
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
#%%
url = '2016_Green_Taxi_Trip_Data.csv'
dftaxi = pd.read_csv(url)
#%%
dftaxi.head()
#print(dftaxi.dtypes)
#%% Convert Objects to timestamps
dftaxi[['lpep_pickup_datetime','Lpep_dropoff_datetime']] = dftaxi[['lpep_pickup_datetime','Lpep_dropoff_datetime']].apply(pd.to_datetime)
print(dftaxi.dtypes)
#%% Substring date from datetime
dftaxi['lpep_pickup_datetime'] = dftaxi['lpep_pickup_datetime'][0:9]
print(dftaxi['lpep_pickup_datetime'])
#%% Transform datetime to daily. Subset to relevant columns.Group data by pick up day. 
#dftaxi.lpep_pickup_datetime.date()
dftaxi = dftaxi[['lpep_pickup_datetime','Lpep_dropoff_datetime','Pickup_longitude','Pickup_latitude','Dropoff_longitude','Dropoff_latitude','Passenger_count','Trip_distance','Total_amount']]
dftaxi.groupby(['lpep_pickup_datetime'])
dftaxi.head()
#%%
dftaxi['response_variable'] = np.where(dftaxi.lpep_pickup_datetime is not None & dftaxi.Lpep_dropoff_datetime is not None, '1',0)
                           #np.where(dftaxi.Lpep_dropoff_datetime is not None,'Dropped off',0))
dftaxi['location_response'] = np.where(dftaxi.Pickup_longitude< 0, '1',0)
dftaxi.head()

#%% Check to ensure that all rows have a response variable
dftaxi[dftaxi['response_variable'] == '0'] 
#returns empty dataframe! 
#%% Ensure data quaility. Do not have incorrect long's in dataset. 
dftaxi[dftaxi['Pickup_longitude'] > 0]                        
#%% QC to check the differences between lat/long and response variable. 7M row discrepancy. 
dftaxi.count()
#%%
#Aggregate by day

#Define seasons