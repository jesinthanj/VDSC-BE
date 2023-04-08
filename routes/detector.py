from app import app
from error_handles import forbidden
from flask import Flask, jsonify, request, render_template


@app.route('/vulnerability-check', methods=['POST', 'GET'])
def getCode():
    # Sample route with a method handlers and a view function
    try:
        text = request.form['myText']
        processed_text = text.upper()
        #print(processed_text)
        return jsonify({'processed_text': processed_text})

    except Exception as e:
        print(e)
