from app import app
from error_handles import forbidden
from flask import Flask, jsonify, request, render_template


@app.route('/get-code', methods=['POST', 'GET'])
def getCode():
    # Sample route with a method handlers and a view function
    try:
        text = request.form['myText']
        print(text)
        
        return text

    except Exception as e:
        print(e)
