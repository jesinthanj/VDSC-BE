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
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
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
    app.run(debug=True)
