# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 16:20:05 2020
@author: vbajaj
"""



##Read Data
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score,mean_squared_error
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pickle



def binarizeVariable(variable, categories):
    if variable == categories[0]:
        return 0
    if variable == categories[1]:
        return 1
    else:
        return None

ins_df = pd.read_csv("https://raw.githubusercontent.com/VasuBajaj/datascience-project-showcase/main/data/insurance.csv")
ins_df_copy =ins_df.copy()
#ins_df = pd.DataFrame(df[:,1:], columns = df[0])
#Method -1 
#values = [ (col, list(ins_df[col].unique())) for col in ins_df.columns if col in ['smoker', 'sex', 'region']]
#print(ins_df['sex'].unique())
#ins_df_copy = ins_df.copy()
#for value in values:
#    key, val = value[0], value[1]
#    if key != 'region':
#        ins_df[key] = ins_df[key] .apply(lambda x : binarizeVariable(x,val) )

#Method - 2
#Covert Gender to Category and rest is taken care
ins_df['sex'] = ins_df['sex'].astype('category')
#print(ins_df['sex'].dtype)
ins_df['sex'] = ins_df['sex'].cat.codes
ins_df['smoker'] = ins_df['smoker'].astype('category')
#print(ins_df['smoker'].dtype)
ins_df['smoker'] = ins_df['smoker'].cat.codes
#print(ins_df.head())
#print(ins_df.info())

#lsex = LabelEncoder()
#lsmoker =  LabelEncoder()
#lregion = LabelEncoder()

#ins_df['sex_n'] = lsex.fit_transform(ins_df['sex'])
#ins_df['smoker_n'] = lsex.fit_transform(ins_df['smoker'])
#ins_df['region_n'] = lsex.fit_transform(ins_df['region'])

##Enable One Hot Encoder

#ins_df = pd.get_dummies(ins_df,columns=['sex','smoker', 'region'])
#ins_df.drop(["sex_1", "smoker_1", "region_southwest"],axis=1, inplace = True)
#print(ins_df)
ins_df.drop(["region"], axis=1, inplace=True)



##Method-3 

#pip install category_encoders

#import category_encoders as ce

#Now we can apply binary encoder as follows:
#binencode=ce.BinaryEncoder(cols=[sex, smoker,‘region’])
#ins_df_binary =binencode.fit_transform(ins_df_copy)
#ins_df_binary

##train and Test Data Set
#print(ins_df.columns.to_list())
ins_df.reindex(['age', 'bmi', 'children', 'sex'\
               , 'smoker', 'charges'])
X = ins_df[['age', 'bmi', 'children', 'sex'\
               , 'smoker']]
y =  ins_df['charges']


# create training and testing vars
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
##print(X_train.shape, y_train.shape)
#print(X_test.shape, y_test.shape)
sc=StandardScaler()
X_train_std=sc.fit_transform(X_train)
X_test_std=sc.transform(X_test)

#Store scalar as pickle Object
scalar = pickle.dump(sc, open('insurance_input_scalar.pkl','wb'))

regressor =  RandomForestRegressor()
regressor.fit(X_train_std, y_train)
y_pred = regressor.predict(X_test_std)

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
#print('RMSE: ', rmse)

#plt.scatter(y_test, y_pred)
#plt.xlabel("True Values")
#plt.ylabel("Predictions")
print("Score:", regressor.score(X_test_std, y_test))

#, columns = ['Test', 'Predicted']
pred = pd.DataFrame([y_test, y_pred])
model = pickle.dump(regressor, open('ipp.pkl','wb'))
#Validate your model
model = pickle.load(open('ipp.pkl','rb'))
result = model.score(X_test_std, y_test)
print(result)
