# -*- coding: utf-8 -*-
"""chicago_crime_rate_prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ApCSdxdOE5a2S5XCZPo88jE1HoYV2MMI
"""

#import requisites library
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
import seaborn as sns

"""
# Chicago Crime Rate Prediction

### More about data



"""

df = pd.read_csv('https://query.data.world/s/6euhafkdlywsiavoyjyybfat42tqsn')

df

df.columns

df.drop(['BEAT', 'WARD', 'FBI CD',
       'X COORDINATE', 'Y COORDINATE', 'LATITUDE', 'LONGITUDE', 'LOCATION', ' SECONDARY DESCRIPTION',
       ' LOCATION DESCRIPTION'], inplace = True, axis =1)

df.columns

df

column_names = [ col.strip().lower().replace(' ', '_') for col in df.columns]

column_names

df.columns = column_names

df

df.drop('case#', inplace = True, axis = 1)

df

df['date__of_occurrence'] = pd.to_datetime(df['date__of_occurrence'], format ='%m/%d/%Y %I:%M:%S %p')

df

df.set_index('date__of_occurrence', inplace = True)

chicago_prophet = df.resample('M').size().reset_index()

chicago_prophet.columns = ['ds','y']
chicago_prophet

m = Prophet()
m.fit(chicago_prophet)

future_df = m.make_future_dataframe(periods = 1000)
forecast = m.predict(future_df)

forecast

figure = m.plot( forecast, xlabel = "Date" , ylabel="Crime Rate")

figure = m.plot_components(forecast)
