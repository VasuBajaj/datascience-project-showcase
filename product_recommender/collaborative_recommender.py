# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 20:48:35 2020

@author: vasubajaj
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from urllib.request import urlopen
from zipfile import ZipFile
import sys
import seaborn as sns

def downloadFile(file_url):
    """Download the file, unzip and load the extract
    args: file_url - url to the file
    """
    url_resp = urlopen(url=file_url)
    tempfileName = "temp_zipfile"
    tempFile = open(tempfileName, "wb")
    tempFile.write(url_resp.read())
    tempFile.close()
    extractFile(tempfileName)

def extractFile(file_name):
    zipped_file = ZipFile(file="temp_zipfile")
    try:
        zipped_file.extractall("")
    except:
        print("Error Occured- ", sys.exc_info()[0])
        

zipurl = 'https://raw.githubusercontent.com/rajeevratan84/datascienceforbusiness/master/ecommerce_data.zip'
downloadFile(zipurl)

def explain_data(df):
    print("*"*80)
    print("\nfeatures: ", df.columns.tolist())
    print("\nmissing values: ", df.isnull().sum().values.sum() )
    print("\nuique values: ", df.nunique())
    print("\ninfo",df.info())
    print("\nrows: ", df.shape[0])
    print("\ncolumns: ", df.shape[1])
    print("*"*80)

#Kagle
def get_numerical_cols(df):
    """

    Returns
    -------
    None.

    """
    num_cols = [col for col in df.columns if df[col].dtype \
                in ["int64","float64"]]
    return num_cols
    
def get_categorical_cols(df):
    """ 
    """
    categeorical_cols = [ col for col in df.columns \
                         if df[col].dtype == 'object' \
                             and df[col].nunique() < 10 ]
    return categeorical_cols
    
    

##Exploratory analysis

df = pd.read_csv("ecommerce_data.csv", encoding = 'ISO-8859-1')
explain_data(df)
num_cols = get_numerical_cols(df)
categeorical_cols = get_categorical_cols(df)
plt.hist(df['Quantity'], bins=5,histtype ='bar', data=None, alpha = 0.7)
plt.xlabel('Dimension')
plt.ylabel('Count')
plt.show()

df.describe()

##Create a correlation plot
df.corr()
plt.figure(figsize=(6,6))
sns.heatmap(df.corr())

#Check for non-relevant and missng values
df.isnull().sum()
df.dropna( subset = ['CustomerID'], inplace=True)
df.shape
df.isnull().sum()


##Create User-Stock Matrix

user_stock_matrix = df.pivot_table(index='CustomerID', values = 'Quantity', \
                                   columns ='StockCode' , aggfunc='sum')
user_stock_matrix.shape
user_stock_matrix = user_stock_matrix.applymap(lambda x : 1 if x > 0 else 0)

#add cosinemetrics
from sklearn.metrics.pairwise import cosine_similarity
cust2cust_sim_matrix = pd.DataFrame(cosine_similarity(user_stock_matrix))
cust2cust_sim_matrix.shape

#Change index Column and columnNames
cust2cust_sim_matrix.columns = user_stock_matrix.index
cust2cust_sim_matrix.index = user_stock_matrix.index

cust2cust_sim_matrix.head()
#user_user_sim_matrix.head()

top_10_sim_users = cust2cust_sim_matrix[12363].sort_values(ascending = False)\
                    .iloc[:10]
                    
most_sim_user = cust2cust_sim_matrix[12363].sort_values(ascending = False).index[1]

# We use the `nonzero` function in the pandas package as it returns the \
#    integer indexes of the elements of the non-zero columns (hence the \
#    items bought).
# We convert to set data type so that we can perform comparison operations \
#    easily afterward.
# See what items were purchased by our customer '12358.0'
items_bought_by_12363 = set(cust2cust_sim_matrix.loc[12363].iloc[cust2cust_sim_matrix.loc[12358]\
                            .to_numpy().nonzero()].index)
items_bought_by_12363

items_bought_by_13027 = set(cust2cust_sim_matrix.loc[13027].iloc[cust2cust_sim_matrix.loc[12358]\
                            .to_numpy().nonzero()].index)
items_bought_by_13027
items_to_recommend_13027 = items_bought_by_12363 - items_bought_by_13027
items_to_recommend_13027
df.loc[df['StockCode'].isin(items_to_recommend_13027), ['StockCode', 'Description']].drop_duplicates().set_index('StockCode')

def get_items_to_recommend_cust(cust_a):
  '''returns the items to recommend to a customer using customer similarity'''
  most_similar_user = cust2cust_sim_matrix.loc[cust_a].sort_values(ascending=False).reset_index().iloc[1, 0]
  items_bought_by_cust_a = set(cust2cust_sim_matrix.loc[cust_a].iloc[cust2cust_sim_matrix.loc[cust_a].to_numpy().nonzero()].index)
  items_bought_by_cust_b = set(cust2cust_sim_matrix.loc[most_similar_user].iloc[cust2cust_sim_matrix.loc[most_similar_user].to_numpy().nonzero()].index)
  items_to_recommend_to_a = items_bought_by_cust_b - items_bought_by_cust_a
  items_description = df.loc[df['StockCode'].isin(items_to_recommend_to_a), ['StockCode', 'Description']].drop_duplicates().set_index('StockCode')
  return items_description

get_items_to_recommend_cust(12358.0)

get_items_to_recommend_cust(12348.0)

df.head()

## ITEM 2 ITEM

# Transposing our customer_item_matrix 
item_item_sim_matrix = pd.DataFrame(cosine_similarity(user_stock_matrix.T))
item_item_sim_matrix.head()

item_item_sim_matrix.shape

# Let's now re-label the columns so that it's easier to understand
# Now let's change the index from 0 to 3665  to the StockCode 

item_item_sim_matrix.columns = user_stock_matrix.T.index

item_item_sim_matrix['StockCode'] = user_stock_matrix.T.index
item_item_sim_matrix = item_item_sim_matrix.set_index('StockCode')
item_item_sim_matrix.head()

# Most similar items to 10080

item_item_sim_matrix.loc['10080'].sort_values(ascending=False)

# Get the top 10 most similar items 
top_10_similar_items = list(item_item_sim_matrix.loc['10080'].sort_values(ascending=False).iloc[:10].index)
top_10_similar_items

# Now let's make a function that returns the most similar items for an inputted item
df.head()

# Get the row information fo a specific item
# Note it occurs multple times, but we need juw the basic info
df.loc[df['StockCode'] == '90210A']

df.loc[df['StockCode'] == '90210A'][:1]

# This code checks our df for stock codes similar to those in our top_10_similar_items, we then display only the Stockcode and Description, remove duplicates
# and ten set the index to StockCode
df.loc[df['StockCode'].isin(top_10_similar_items), ['StockCode', 'Description']].drop_duplicates().set_index('StockCode').loc[top_10_similar_items]

def get_top_similar_items(item):
  top_10_similar_items = list(item_item_sim_matrix.loc[item].sort_values(ascending=False).iloc[:10].index)
  top_10 = df.loc[df['StockCode'].isin(top_10_similar_items), ['StockCode', 'Description']].drop_duplicates().set_index('StockCode').loc[top_10_similar_items]
  return top_10

get_top_similar_items('84029E')


## Genrate the models and save then

import pickle
cust2cust = pickle.dump()



