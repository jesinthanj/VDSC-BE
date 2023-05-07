from app import app
from functions import codemetrics
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

@app.route('/vulnerability-test', methods=['POST', 'GET'])
def testCode():
    try:
        with open('model/tokenizer.pickle', 'rb') as handle:
            tokenizer= pickle.load(handle)

        tokenizer

        model = tf.keras.models.load_model("model/vulcnn.h5")

        source_code = request.form['myText']
        #source_code ="static void goodG2B2() size_t data ; data = 0;if ( STATIC_CONST_FIVE == 5 )data = 20;if ( STATIC_CONST_FIVE == 5 )char * myString ;if ( data > strlen ( HELLO_STRING ) )myString = ( char * ) malloc ( data * sizeof ( char ) ); strcpy ( myString , HELLO_STRING ); printLine ( myString ); void printLine (const char * line) if ( line != NULL )printf ( ""%s\n"" , line ); free ( myString );"

        list_tokenized_text = tokenizer.texts_to_sequences(source_code)
        print(source_code)

        data = tf.keras.preprocessing.sequence.pad_sequences(list_tokenized_text,
                                                                        maxlen=500,
                                                                        padding='post',
                                                            dtype=object)
        data = data.astype(np.int64)

        predicted = model.predict(data)

        pred_test = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

        for col in range(0,len(predicted)):
            for i, row in enumerate(predicted[col]):
                if row[0] >= row[1]:
                    pred_test[col].append(0)
                else:
                    pred_test[col].append(1)

        for col in range(0,len(pred_test)):
            print(pd.value_counts(pred_test[col]))
        

        column_names = ['CWE114', 'CWE134', 'CWE190', 'CWE196', 'CWE319', 'CWE369', 'CWE398',
                    'CWE416', 'CWE427', 'CWE469', 'CWE506', 'CWE605', 'CWE606', 'CWE666',
                    'CWE680', 'CWE761', 'CWE789']

        indices = [[i for i, val in enumerate(col) if val == 1] for col in pred_test]

        indices_list = [i for i, col in enumerate(pred_test) if any(val == 1 for val in col)]
        i=[str(index) for index in indices_list]
        res_i="".join(i)
        res=int(res_i)
        vulnerableClass = column_names[res]
        print("The vulnerability class detected is: ",vulnerableClass)


        words=[]
        for index in indices:
            if len(index) > 0:
                for i in index:
                        predicted_word = tokenizer.index_word[i]
                        words.append(predicted_word)
                        
                        
        def highlight_words(sentence, words):
            highlighted_sentence = sentence
            for word in words:       
                highlighted_word = f"\033[91m{word}\033[0m"  # Use ANSI escape codes for red color
                #highlighted_word = f'<span style="color: red;">{word}</span>'
                highlighted_sentence = highlighted_sentence.replace(word, highlighted_word)
            return highlighted_sentence

        sentence = source_code
        highlighted_words = words
        highlighted_sentence = highlight_words(sentence, highlighted_words)

        print()
        print("Localized code:")
        print()
        print(highlighted_sentence)
        metrics=codemetrics.calculate_code_metrics(source_code)

        return jsonify({"processed_text":highlighted_sentence,"code_metrics":metrics, "vulnerable_class":vulnerableClass})
    except Exception as e:
        print(e)
