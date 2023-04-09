from flask import Flask
from flask import render_template
from flask.helpers import send_from_directory
import os

from dotenv import load_dotenv

app = Flask(__name__, static_url_path='', static_folder='.')
app.config['CORS_HEADERS'] = 'Content-Type'

# Load environment variables
load_dotenv()


@app.after_request
def after_request_func(response):
    # CORS section
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    response.headers['Cache-Control'] = 'no-cache'
    return response
# end CORS section


import error_handles

# Add your API endpoints here
from routes import detector
# from routes import cars
# ...


@app.route('/')
def home_page():
    try:
        return render_template('home.html')

    except Exception as e:
        print(e)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
