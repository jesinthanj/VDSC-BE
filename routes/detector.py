from app import app
from functions import codemetrics
from dataset import description
from error_handles import forbidden
from flask import Flask, jsonify, request, render_template
import time
import pandas as pd
import numpy as np
import tensorflow as tf
import pickle


@app.route('/vulnerability-check', methods=['POST', 'GET'])
def getCode():
    try:
        with open('model/tokenizer.pickle', 'rb') as handle:
            tokenizer = pickle.load(handle)

        tokenizer

        model = tf.keras.models.load_model("model/vulcnn.h5")

        source_code = request.form['myText']

        list_tokenized_text = tokenizer.texts_to_sequences(source_code)
        # print(source_code)

        data = tf.keras.preprocessing.sequence.pad_sequences(list_tokenized_text,
                                                             maxlen=500,
                                                             padding='post',
                                                             dtype=object)
        data = data.astype(np.int64)

        predicted = model.predict(data)

        pred_test = [[], [], [], [], [], [], [],
                     [], [], [], [], [], [], [], [], [], []]

        for col in range(0, len(predicted)):
            for i, row in enumerate(predicted[col]):
                if row[0] >= row[1]:
                    pred_test[col].append(0)
                else:
                    pred_test[col].append(1)

        # for col in range(0,len(pred_test)):
        #     print(pd.value_counts(pred_test[col]))

        column_names = ['CWE114', 'CWE134', 'CWE190', 'CWE196', 'CWE319', 'CWE369', 'CWE398',
                        'CWE416', 'CWE427', 'CWE469', 'CWE506', 'CWE605', 'CWE606', 'CWE666',
                        'CWE680', 'CWE761', 'CWE789']

        indices = [[i for i, val in enumerate(
            col) if val == 1] for col in pred_test]

        indices_list = [i for i, col in enumerate(
            pred_test) if any(val == 1 for val in col)]
        i = [str(index) for index in indices_list]
        res_i = "".join(i)
        res = int(res_i)
        vulnerableClass = column_names[res]
        print("The vulnerability class detected is: ", vulnerableClass)

        words = []
        for index in indices:
            if len(index) > 0:
                for i in index:
                    predicted_word = tokenizer.index_word[i]
                    words.append(predicted_word)

        def highlight_words(sentence, words):
            highlighted_sentence = sentence
            for word in words:
                # Use ANSI escape codes for red color
                highlighted_word = f"\033[91m{word}\033[0m"
                highlighted_sentence = highlighted_sentence.replace(
                    word, highlighted_word)
            return highlighted_sentence

        sentence = source_code
        highlighted_words = words
        highlighted_sentence = highlight_words(sentence, highlighted_words)

        metrics = codemetrics.calculate_code_metrics(source_code)
        class_desc = description.description(vulnerableClass)

        return jsonify({"processed_text": highlighted_sentence, "code_metrics": metrics, "vulnerable_class": vulnerableClass, "description": class_desc})
    except Exception as e:
        print(e)
