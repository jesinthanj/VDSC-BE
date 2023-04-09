from app import app
from error_handles import forbidden
from flask import Flask, jsonify, request, render_template
import time
import pandas as pd 
import numpy as np
import tensorflow as tf
import pickle


@app.route('/vulnerability-check', methods=['POST', 'GET'])
def getCode():
    # Sample route with a method handlers and a view function
    start_time = time.time()
    try:
        source_code = request.form['myText']

        with open('Model/tokenizer.pickle', 'rb') as handle:
            tokenizer= pickle.load(handle)

        tokenizer

        #print(source_code)
        x = source_code
        list_tokenized_text = tokenizer.texts_to_sequences(x)
        #print(x)


        data = tf.keras.preprocessing.sequence.pad_sequences(list_tokenized_text, maxlen=500, padding='post', dtype=object)
        data = data.astype(np.int64)

        model = tf.keras.models.load_model("Model/vuldet.h5")

        #model.summary()

        predicted = model.predict(data)

        pred_test = [[],[],[],[],[]]

        for col in range(0,len(predicted)):
            for row in predicted[col]:
                if row[0] >= row[1]:
                    pred_test[col].append(0)
                else:
                    pred_test[col].append(1)
                    

        # for col in range(0,len(pred_test)):
        #     print(pd.value_counts(pred_test[col]))

        #print(pred_test)
        end_time=time.time()
        return jsonify({"processed_text":pred_test,"result":(end_time-start_time)})
    except Exception as e:
        print(e)
