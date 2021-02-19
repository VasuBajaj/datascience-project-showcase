import pandas as pd
from sklearn.linear_model import LogisticRegression
#from utils import utils
# create df
#train = pd.read_csv('https://raw.githubusercontent.com/elizabethts/deploy-mlm-flask-heroku/master/titanic.csv') # change file path
#train = utils.get_dataframe('./data/titanic.csv') #
train = pd.read_csv('./data/titanic.csv')
# drop null values
train.dropna(inplace=True)
# features and target
target = 'Survived'
features = ['Pclass', 'Age', 'SibSp', 'Fare']
# X matrix, y vector
X = train[features]
y = train[target]
# model 
model = LogisticRegression()
model.fit(X, y)
print(model.score(X, y))

import pickle
pickle.dump(model, open('./model/model.pkl', 'wb'))