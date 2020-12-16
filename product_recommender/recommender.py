# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 18:37:28 2020

@author: vasubajaj
"""

# Loading our data
# specify encoding to deal with different formats
#df = pd.read_csv('./data/ecommerce/data.csv', encoding = 'ISO-8859-1')

# Download and unzip our zipfile
from urllib.request import urlopen
from zipfile import ZipFile
import pandas as pd

class GetZipFileException(Exception):
    """ Raise Exception if the code to get the zip url fails.
    Attributes:
        boolenFlag -- input booleanFlag which caused the error
        message -- explanation of the error 
    """
    def __init__(self, boolenFlag, message="Unzipping zip file failed"):
        self.boolenFlag = boolenFlag
        self.message = message
        super().__init__(self.message)

def getDataFile(url):
    zipresp = urlopen(url) # Create a new file on the hard drive
    tempzip = open("tempfile.zip", "wb") # Write the contents of the \
                                            #downloaded file into the new file
    tempzip.write(zipresp.read()) # Close the newly-created file
    tempzip.close() # Re-open the newly-created file with ZipFile()
    zf = ZipFile("tempfile.zip") # Extract its contents into <extraction_path>
    zf.extractall(path = '') # note that extractall will automatically create \
                            #the path, left blank so it's in working directory
    zf.close() # close the ZipFile instance
    return True

def summarizeData(df):
    # View a summary of our data
    print('*'*80)
    print ("Rows     : " , df.shape[0])
    print ("Columns  : " , df.shape[1])
    print ("\nFeatures : \n" , df.columns.tolist())
    print ("\nMissing values :  ", df.isnull().sum().values.sum())
    print ("\nUnique values :  \n", df.nunique())
    print('*'*80)
    

zipurl = 'https://raw.githubusercontent.com/rajeevratan84/datascienceforbusiness/master/ecommerce_data.zip'
#if ~getDataFile(zipurl):
#    raise GetZipFileException(False)

df = pd.read_csv("ecommerce_data.csv", encoding = 'ISO-8859-1')
summarizeData(df)

# Statistics on our numeric columns
df.describe()

# Removing cancelled orders (shown as negative values in Quantity)
df = df.loc[df['Quantity'] > 0]
df = df.loc[df['UnitPrice'] > 0]

# Statistics on our numeric columns
df.describe()

# Check for null values
print(df.isnull().sum())

# Lets see how these records with missing customer ID look
print(df.loc[df['CustomerID'].isna()].head())

# Number of records and shape before dropping our missing values
print(df.shape)

# Let's drop these records since we can't build our required matrixes 
df = df.dropna(subset=['CustomerID'])

# Number of records after dropping our missing values
print(df.shape)

# Check for null values
df.isnull().sum()

# We need a create a matrix that contains the customer IDs as the index, and \
# each invidividual item as a column
# We use the pivot function to use the CustomerID as the index and use the \
#    StockCode as columns
# Then we using the Quantity value as the values we display, and finally use \
# the aggfunc to sum up these values

customer_item_matrix = df.pivot_table(index='CustomerID', columns='StockCode'\
                                      , values='Quantity',aggfunc='sum')
customer_stock_matrix = df.pivot_table(index = , columns = , values='Quantity', aggfunc = 'sum')
customer_item_matrix.head()
customer_item_matrix.shape

# We have quanties, but we don't actually need the exact numbers
# Let's now change all the NaNs to 0 and all values above 1 to 1
#
customer_item_matrix = customer_item_matrix.applymap(lambda x: 1 if x > 0 else 0 )
customer_item_matrix.head()
customer_item_matrix.shape


# import our cosine_similarity function from sklearn
from sklearn.metrics.pairwise import cosine_similarity

# Let's use the sklearn cosine_similarity function to compute the pairwise cosine similarities between the cusomters 

user_user_sim_matrix = pd.DataFrame(cosine_similarity(customer_item_matrix))
user_user_sim_matrix

# Also let's check out the shape, it should be a square matrix (i.e. same width and length)
user_user_sim_matrix.shape

# Let's now re-label the columns so that it's easier to understand
# Now let's change the index from 0 to 4339 to the Customer IDs 

user_user_sim_matrix.columns = customer_item_matrix.index

user_user_sim_matrix['CustomerID'] = customer_item_matrix.index

user_user_sim_matrix = user_user_sim_matrix.set_index('CustomerID')
user_user_sim_matrix.head()

# Sort on the customers most similar to 12358
user_user_sim_matrix.loc[12358].sort_values(ascending=False)

# We use the `nonzero` function in the pandas package as it returns the \
#    integer indexes of the elements of the non-zero columns (hence the \
#    items bought).
# We convert to set data type so that we can perform comparison operations \
#    easily afterward.
# See what items were purchased by our customer '12358.0'
items_bought_by_12358 = set(customer_item_matrix.loc[12358].iloc[customer_item_matrix.loc[12358].to_numpy().nonzero()].index)
items_bought_by_12358

# Let's see what customer 14145.0 bought
items_bought_by_14145 = set(customer_item_matrix.loc[14145.0].iloc[customer_item_matrix.loc[14145.0].to_numpy().nonzero()].index)
items_bought_by_14145

# What items did 12358 buy, but 14145 didn't buy?
# Those would be good items to recommend to 14145 since they're so similar
items_to_recommend_to_14145 = items_bought_by_12358 - items_bought_by_14145
items_to_recommend_to_14145

# Let's get the descriptions of these items 
df.loc[df['StockCode'].isin(items_to_recommend_to_14145), ['StockCode', 'Description']].drop_duplicates().set_index('StockCode')

most_similar_user = user_user_sim_matrix.loc[12358].sort_values(ascending=False).reset_index().iloc[1, 0]
most_similar_user

def get_items_to_recommend_cust(cust_a):
  '''returns the items to recommend to a customer using customer similarity'''
  most_similar_user = user_user_sim_matrix.loc[cust_a].sort_values(ascending=False).reset_index().iloc[1, 0]
  items_bought_by_cust_a = set(customer_item_matrix.loc[cust_a].iloc[customer_item_matrix.loc[cust_a].to_numpy().nonzero()].index)
  items_bought_by_cust_b = set(customer_item_matrix.loc[most_similar_user].iloc[customer_item_matrix.loc[most_similar_user].to_numpy().nonzero()].index)
  items_to_recommend_to_a = items_bought_by_cust_b - items_bought_by_cust_a
  items_description = df.loc[df['StockCode'].isin(items_to_recommend_to_a), ['StockCode', 'Description']].drop_duplicates().set_index('StockCode')
  return items_description

get_items_to_recommend_cust(12358.0)

get_items_to_recommend_cust(12348.0)

df.head()

# Transposing our customer_item_matrix 
item_item_sim_matrix = pd.DataFrame(cosine_similarity(customer_item_matrix.T))
item_item_sim_matrix.head()

item_item_sim_matrix.shape

# Let's now re-label the columns so that it's easier to understand
# Now let's change the index from 0 to 3665  to the StockCode 

item_item_sim_matrix.columns = customer_item_matrix.T.index

item_item_sim_matrix['StockCode'] = customer_item_matrix.T.index
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


