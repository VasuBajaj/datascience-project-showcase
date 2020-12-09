# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 11:36:07 2020

@author: vbajaj
"""

import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import logging

app = Flask(__name__)
logging.basicConfig(filename = 'mainApp.log',format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('loading pickled model..')
scalar = pickle.load(open('insurance_input_scalar.pkl','rb'))
model = pickle.load(open('ipp.pkl','rb'))

@app.route('/')
def home():
    return render_template("insurance_premium_predictor_home.html")

def binarizeVariable(value):
    if value.lower() == 'yes':
        return 1
    elif value.lower() == 'no':
        return 0
    elif value.lower() == 'female':
        return 0
    elif value.lower() == 'male':
        return 1
    else:
        return None
        
    
@app.route('/predictInsurance',methods=['POST'])  
def predictInsurance():
    """This method predicts the insurance value for an individual based on input
    
    args:
    return:
    """
    logging.info(request.form.values())
    int_features = [x for x in request.form.values()]
    name = int_features[0]
    logging.info(int_features)
    age = int_features[1]
    bmi = int_features[2]
    children= int_features[3]
    sex = binarizeVariable(int_features[4])
    smoker = binarizeVariable(int_features[5])
    final_features = [np.array([age, bmi, children,sex,smoker])]
    prediction = model.predict(scalar.transform(final_features))

    output = round(prediction[0], 2)
    logging.info(output)
    return render_template("insurance_premium_predictor_home.html", prediction_text='Hi {name}, your Insurance Premium could be Rs: {output}'.format(name= name, output=output))
    


if __name__ == "__main__":
    app.run(debug=True)