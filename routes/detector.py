from app import app
from error_handles import forbidden
from flask import Flask, jsonify, request, render_template
import time


@app.route('/vulnerability-check', methods=['POST', 'GET'])
def getCode():
    # Sample route with a method handlers and a view function
    start_time = time.time()
    try:
        
        text = request.form['myText']
        processed_text = text.upper()
        end_time = time.time()
        return jsonify({'processed_text': processed_text, 'result': f"Changes : Lower to upper case \nTime Taken : {end_time-start_time}"})

    except Exception as e:
        print(e)
